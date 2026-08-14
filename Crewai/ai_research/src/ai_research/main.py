#!/usr/bin/env python
import sys
from .crew import AiResearch


def run():
    """
    Run the AI Research crew.
    """

    topic = input("Enter the research topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        sys.exit(1)

    inputs = {
        "topic": topic
    }

    print("\n======================================")
    print("      AI RESEARCH CREW")
    print("======================================")
    print(f"Topic: {topic}\n")

    try:
        result = AiResearch().crew().kickoff(inputs=inputs)

        print("\n======================================")
        print("        RESEARCH COMPLETED")
        print("======================================")

        print(result)

    except Exception as e:
        print("\nCrew execution failed:")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    run()