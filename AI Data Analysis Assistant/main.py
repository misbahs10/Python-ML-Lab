"""
main.py
--------
AI Data Analysis Assistant - Track A (Explorer)

Flow:
1. Load the CSV dataset
2. Display basic dataset info
3. Compute and display statistics
4. Answer 3 fixed natural language questions
5. Generate one chart
6. Generate an AI explanation of the result (Groq API)
"""

from dotenv import load_dotenv

import analysis
import visualization
import ai_explainer

DATASET_PATH = "dataset.csv"

# The 3 fixed questions judges will ask
QUESTIONS = [
    "Which department has the highest attrition rate?",
    "What is the average monthly income of employees?",
    "Which job role has the maximum number of employees?",
]


def main():
    load_dotenv()  # loads GROQ_API_KEY from a .env file if present

    # Step 1: Load dataset
    df = analysis.load_dataset(DATASET_PATH)
    analysis.show_basic_info(df)

    # Step 2: Analyze dataset
    stats = analysis.compute_statistics(df)
    analysis.print_statistics(stats)

    # Step 3: Answer fixed natural language questions
    print("=" * 60)
    print("QUESTION & ANSWER SECTION")
    print("=" * 60)
    for q in QUESTIONS:
        print(f"Q: {q}")
        print(f"A: {analysis.answer_question(df, q)}\n")

    # Step 4: Generate chart
    chart_path = visualization.generate_attrition_chart(df)
    print(f"Chart saved to: {chart_path}\n")

    # Step 5: AI explanation
    print("=" * 60)
    print("AI EXPLANATION")
    print("=" * 60)
    explanation = ai_explainer.generate_explanation(stats)
    print(explanation)


if __name__ == "__main__":
    main()