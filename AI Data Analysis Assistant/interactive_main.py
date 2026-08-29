"""
interactive_main.py
---------------------
Interactive version of the AI Data Analysis Assistant.

Same Steps 1, 2, 4, 5 as main.py (load, analyze, chart, explanation),
but Step 3 becomes a live loop: the user can type ANY question about
the dataset, and the program keeps answering until the user types
'exit' / 'quit'.
"""

from dotenv import load_dotenv

import analysis
import visualization
import ai_explainer
import interactive_qa

DATASET_PATH = "dataset.csv"
EXIT_WORDS = {"exit", "quit", "bye", "stop", "q"}


def main():
    load_dotenv()

    # Step 1: Load dataset
    df = analysis.load_dataset(DATASET_PATH)
    analysis.show_basic_info(df)

    # Step 2: Analyze dataset
    stats = analysis.compute_statistics(df)
    analysis.print_statistics(stats)

    # Step 4: Generate chart (do it once up front)
    chart_path = visualization.generate_attrition_chart(df)
    print(f"Chart saved to: {chart_path}\n")

    # Step 5: AI explanation of the main finding
    print("=" * 60)
    print("AI EXPLANATION")
    print("=" * 60)
    print(ai_explainer.generate_explanation(stats))
    print()

    # Step 3 (interactive): free-form Q&A loop
    print("=" * 60)
    print("ASK ME ANYTHING ABOUT THE DATASET")
    print("(type 'exit' or 'quit' to stop)")
    print("=" * 60)

    while True:
        question = input("\nYour question: ").strip()

        if question.lower() in EXIT_WORDS:
            print("Exiting the AI Data Analysis Assistant. Goodbye!")
            break

        if not question:
            print("Please type a question, or 'exit' to quit.")
            continue

        answer = interactive_qa.answer_any_question(df, question)
        print(f"Answer: {answer}")


if __name__ == "__main__":
    main()