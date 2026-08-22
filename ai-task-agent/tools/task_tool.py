# tools/task_tool.py

def save_note(text: str) -> str:
    """Note ya task ko file me save karta hai."""
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "Note saved successfully."