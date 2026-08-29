"""
interactive_qa.py
-------------------
Answers ANY free-form question about the dataset (not just the 3 fixed ones).

Approach (kept simple and explainable for interview purposes):
1. Try to understand the question using keyword + column matching
   (rule-based, pure Python/Pandas - fast and free).
2. If the rule-based engine cannot confidently answer, fall back to
   the Groq LLM, giving it a short statistical summary of the dataset
   as context so it can reason about the answer.
"""

import os
import pandas as pd
from groq import Groq

# Map common everyday words -> actual dataset column names
COLUMN_SYNONYMS = {
    "income": "MonthlyIncome",
    "salary": "MonthlyIncome",
    "pay": "MonthlyIncome",
    "age": "Age",
    "department": "Department",
    "dept": "Department",
    "role": "JobRole",
    "job role": "JobRole",
    "position": "JobRole",
    "attrition": "Attrition",
    "leaving": "Attrition",
    "left the company": "Attrition",
    "left": "Attrition",
    "quit": "Attrition",
    "resign": "Attrition",
    "distance": "DistanceFromHome",
    "commute": "DistanceFromHome",
    "experience": "TotalWorkingYears",
    "working years": "TotalWorkingYears",
    "tenure": "YearsAtCompany",
    "years at company": "YearsAtCompany",
    "overtime": "OverTime",
    "gender": "Gender",
    "satisfaction": "JobSatisfaction",
    "education": "Education",
    "performance": "PerformanceRating",
    "hike": "PercentSalaryHike",
    "raise": "PercentSalaryHike",
    "marital": "MaritalStatus",
    "companies worked": "NumCompaniesWorked",
    "training": "TrainingTimesLastYear",
    "promotion": "YearsSinceLastPromotion",
    "manager": "YearsWithCurrManager",
    "work life balance": "WorkLifeBalance",
    "travel": "BusinessTravel",
}

# Direct value -> column lookup (for specific category names like "Sales", "male")
KNOWN_VALUES = {
    "male": ("Gender", "Male"),
    "female": ("Gender", "Female"),
    "sales": ("Department", "Sales"),
    "human resources": ("Department", "Human Resources"),
    "research & development": ("Department", "Research & Development"),
    "research and development": ("Department", "Research & Development"),
    "married": ("MaritalStatus", "Married"),
    "single": ("MaritalStatus", "Single"),
    "divorced": ("MaritalStatus", "Divorced"),
}


def _find_column(question: str):
    """Find the most likely column referenced in a question."""
    q = question.lower()
    # check longer phrases first so "job role" matches before "role" ambiguity etc.
    for phrase in sorted(COLUMN_SYNONYMS.keys(), key=len, reverse=True):
        if phrase in q:
            return COLUMN_SYNONYMS[phrase]
    return None


def _rule_based_answer(df: pd.DataFrame, question: str):
    """Try to answer using simple keyword rules. Returns None if unsure."""
    q = question.lower()

    # Handle compound questions joined with "and" (answer each part separately)
    if " and what" in q or "? and" in q or " and how" in q or " and which" in q:
        parts = [p.strip() for p in question.replace("?", "?|").split("|") if p.strip()]
        if len(parts) < 2:
            parts = [p.strip() for p in question.split(" and ") if p.strip()]
        answers = []
        for part in parts:
            sub_answer = _rule_based_answer(df, part)
            if sub_answer:
                answers.append(sub_answer)
        if len(answers) >= 2:
            return "\n".join(answers)
        # if we couldn't confidently split, fall through to normal handling

    # Special case: gender breakdown (male and female mentioned together)
    if "male" in q and "female" in q:
        counts = df["Gender"].value_counts().to_dict()
        return f"There are {counts.get('Male', 0)} male and {counts.get('Female', 0)} female employees."

    # Special case: a specific known category value (e.g. "Sales", "Married")
    for value_key, (col, actual_value) in KNOWN_VALUES.items():
        if value_key in q and any(w in q for w in ["how many", "count", "number of"]):
            count = (df[col] == actual_value).sum()
            return f"{count} employees have {col} = '{actual_value}'."

    # Special case: attrition rate broken down by department
    if "attrition" in q and ("department" in q or "dept" in q):
        rate = (
            df[df["Attrition"] == "Yes"].groupby("Department").size()
            / df.groupby("Department").size()
            * 100
        ).round(2)
        if any(word in q for word in ["highest", "most", "maximum"]):
            dept = rate.idxmax()
            return f"The '{dept}' department has the highest attrition rate at approximately {rate.max()}%."
        if any(word in q for word in ["lowest", "least", "minimum"]):
            dept = rate.idxmin()
            return f"The '{dept}' department has the lowest attrition rate at approximately {rate.min()}%."
        return f"Attrition rate by department (%):\n{rate.to_string()}"

    col = _find_column(question)

    if col is None:
        return None

    is_numeric = pd.api.types.is_numeric_dtype(df[col])

    # Average / mean
    if any(word in q for word in ["average", "mean", "avg"]) and is_numeric:
        return f"The average {col} is approximately {round(df[col].mean(), 2)}."

    # Highest / maximum / most
    if any(word in q for word in ["highest", "maximum", "max", "most"]):
        if is_numeric:
            return f"The highest {col} is {df[col].max()}."
        else:
            top = df[col].value_counts().idxmax()
            count = df[col].value_counts().max()
            return f"'{top}' is the most common value for {col}, appearing {count} times."

    # Lowest / minimum / least
    if any(word in q for word in ["lowest", "minimum", "min", "least"]):
        if is_numeric:
            return f"The lowest {col} is {df[col].min()}."
        else:
            bottom = df[col].value_counts().idxmin()
            count = df[col].value_counts().min()
            return f"'{bottom}' is the least common value for {col}, appearing {count} times."

    # Count / how many
    if any(word in q for word in ["how many", "count", "number of"]):
        if is_numeric:
            return f"There are {df[col].count()} recorded values for {col}."
        else:
            return f"Value counts for {col}:\n{df[col].value_counts().to_string()}"

    # Distribution / breakdown
    if any(word in q for word in ["distribution", "breakdown", "spread"]):
        if is_numeric:
            return f"Summary for {col}:\n{df[col].describe().round(2).to_string()}"
        else:
            return f"Distribution for {col}:\n{df[col].value_counts().to_string()}"

    return None


def _llm_answer(question: str, df: pd.DataFrame) -> str:
    """Fallback: ask Groq's LLM using a compact statistical summary as context."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return (
            "I couldn't match this question to a known pattern, and no Groq API "
            "key is configured to ask the AI. Try rephrasing your question "
            "(e.g. mention a column like income, department, age, attrition)."
        )

    # Build a compact context so we don't send the whole dataset
    numeric_summary = df.describe().round(2).to_string()
    categorical_cols = df.select_dtypes(include="object").columns[:6]
    categorical_summary = "\n".join(
        f"{c}: {df[c].value_counts().to_dict()}" for c in categorical_cols
    )

    prompt = (
        "You are a data analysis assistant. Based ONLY on the statistics below "
        "(from an HR Employee Attrition dataset), answer the user's question "
        "concisely in 1-3 sentences.\n\n"
        f"Numeric summary:\n{numeric_summary}\n\n"
        f"Categorical summary:\n{categorical_summary}\n\n"
        f"Question: {question}"
    )

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI call failed: {e}] Could not answer this question."


def answer_any_question(df: pd.DataFrame, question: str) -> str:
    """Main entry point: try rule-based first, then fall back to the LLM."""
    answer = _rule_based_answer(df, question)
    if answer is not None:
        return answer
    return _llm_answer(question, df)