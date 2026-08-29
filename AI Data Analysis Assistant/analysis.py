"""
analysis.py
------------
Handles: loading the CSV dataset, showing basic dataset info,
computing useful statistics, and answering fixed natural language
questions about the dataset.
"""

import pandas as pd


def load_dataset(path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    df = pd.read_csv(path)
    return df


def show_basic_info(df: pd.DataFrame) -> None:
    """Print basic information about the dataset (Step 1)."""
    print("=" * 60)
    print("DATASET BASIC INFORMATION")
    print("=" * 60)
    print(f"Number of rows      : {df.shape[0]}")
    print(f"Number of columns   : {df.shape[1]}")
    print(f"Column names        : {list(df.columns)}")
    print("\nMissing values per column:")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    print(missing if not missing.empty else "No missing values found.")
    print("\nData types:")
    print(df.dtypes)
    print()


def compute_statistics(df: pd.DataFrame) -> dict:
    """Compute useful summary statistics (Step 2)."""
    stats = {}

    stats["total_records"] = len(df)

    # Numeric summaries
    stats["avg_monthly_income"] = round(df["MonthlyIncome"].mean(), 2)
    stats["max_monthly_income"] = int(df["MonthlyIncome"].max())
    stats["min_monthly_income"] = int(df["MonthlyIncome"].min())
    stats["avg_age"] = round(df["Age"].mean(), 2)

    # Category distributions
    stats["attrition_counts"] = df["Attrition"].value_counts().to_dict()
    stats["department_counts"] = df["Department"].value_counts().to_dict()
    stats["jobrole_counts"] = df["JobRole"].value_counts().to_dict()

    # Attrition rate by department (%)
    attrition_by_dept = (
        df[df["Attrition"] == "Yes"]
        .groupby("Department")
        .size()
        / df.groupby("Department").size()
        * 100
    ).round(2)
    stats["attrition_rate_by_department"] = attrition_by_dept.to_dict()

    return stats


def print_statistics(stats: dict) -> None:
    print("=" * 60)
    print("DATASET STATISTICS")
    print("=" * 60)
    print(f"Total records            : {stats['total_records']}")
    print(f"Average Monthly Income   : {stats['avg_monthly_income']}")
    print(f"Max Monthly Income       : {stats['max_monthly_income']}")
    print(f"Min Monthly Income       : {stats['min_monthly_income']}")
    print(f"Average Age              : {stats['avg_age']}")
    print(f"Attrition counts         : {stats['attrition_counts']}")
    print(f"Department counts        : {stats['department_counts']}")
    print(f"Attrition rate by dept % : {stats['attrition_rate_by_department']}")
    print()


# ---------------------------------------------------------------------
# Step 3: Answering fixed natural language questions (rule-based logic)
# ---------------------------------------------------------------------

def answer_highest_attrition_department(df: pd.DataFrame) -> str:
    rate = (
        df[df["Attrition"] == "Yes"]
        .groupby("Department")
        .size()
        / df.groupby("Department").size()
        * 100
    )
    dept = rate.idxmax()
    pct = round(rate.max(), 2)
    return f"The '{dept}' department has the highest attrition rate at approximately {pct}%."


def answer_average_monthly_income(df: pd.DataFrame) -> str:
    avg_income = round(df["MonthlyIncome"].mean(), 2)
    return f"The average monthly income of employees is approximately {avg_income}."


def answer_most_common_job_role(df: pd.DataFrame) -> str:
    role = df["JobRole"].value_counts().idxmax()
    count = df["JobRole"].value_counts().max()
    return f"'{role}' is the most common job role, with {count} employees."


# Fixed questions mapped to their handler functions
FIXED_QUESTIONS = {
    "Which department has the highest attrition rate?": answer_highest_attrition_department,
    "What is the average monthly income of employees?": answer_average_monthly_income,
    "Which job role has the maximum number of employees?": answer_most_common_job_role,
}


def answer_question(df: pd.DataFrame, question: str) -> str:
    """Answer a fixed natural language question using rule-based logic."""
    handler = FIXED_QUESTIONS.get(question)
    if handler is None:
        return "Sorry, this question is not recognized by the assistant."
    return handler(df)