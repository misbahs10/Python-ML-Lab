import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from qa_chain import ask_question #type: ignore


def print_banner():
    print("=" * 50)
    print("📄 RAG Application — Document Q&A")
    print("=" * 50)
    print("Apni documents ke baare mein sawal poocho.")
    print("Exit karne ke liye 'exit' ya 'quit' likho.\n")


def main():
    print_banner()

    while True:
        query = input("❓ Aapka sawal: ").strip()

        if query.lower() in ["exit", "quit", "q"]:
            print("👋 Chalte hain, phir milte hain!")
            break

        if not query:
            continue

        print("\n🔍 Sochte hain...\n")
        answer, sources = ask_question(query)

        print(f"💡 Answer:\n{answer}\n")
        print("📚 Sources:")
        for i, doc in enumerate(sources):
            print(f"  [{i+1}] {doc.metadata.get('source')} (page {doc.metadata.get('page')})")
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()