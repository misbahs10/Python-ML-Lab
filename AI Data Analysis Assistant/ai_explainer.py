"""
ai_explainer.py
----------------
Handles the single LLM API call (Step 5 + AI Integration).
Uses the Groq API to generate a short, easy-to-understand
explanation of the chart / analysis result.
"""

import os
from groq import Groq


def generate_explanation(stats: dict) -> str:
    """
    Send the key statistics to Groq's LLM and get back a short,
    simple explanation of the findings (similar to the example in the
    task document).
    Falls back to a rule-based explanation if no API key is configured
    or the API call fails, so the app still runs end-to-end.
    """
    attrition_rate = stats["attrition_rate_by_department"]
    top_dept = max(attrition_rate, key=attrition_rate.get)
    top_rate = attrition_rate[top_dept]

    prompt = (
        "You are a data analyst assistant. In 2-3 simple sentences, "
        "explain the following finding for a non-technical audience:\n\n"
        f"The '{top_dept}' department has the highest employee attrition rate "
        f"at {top_rate}%, compared to other departments in the company. "
        f"The average monthly income across all employees is {stats['avg_monthly_income']}.\n\n"
        "Keep it clear, short, and easy to understand."
    )

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _fallback_explanation(top_dept, top_rate)

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Warning] Groq API call failed ({e}). Using fallback explanation.\n")
        return _fallback_explanation(top_dept, top_rate)


def _fallback_explanation(top_dept: str, top_rate: float) -> str:
    """Simple rule-based explanation used if the API is unavailable."""
    return (
        f"The '{top_dept}' department shows the highest employee attrition, "
        f"with approximately {top_rate}% of its employees leaving the company. "
        "This suggests the company may want to investigate working conditions "
        "or job satisfaction specifically within this department."
    )