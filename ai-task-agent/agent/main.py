# agent/main.py
import os
import sys
import json
from dotenv import load_dotenv
from groq import Groq #type: ignore

# tools folder ko path me add karna (taake import ho sake)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from tools.calculator_tool import calculate
from tools.search_tool import search_web
from tools.task_tool import save_note

load_dotenv()  # .env se API keys load karta hai

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Groq ko batana ke kaunse tools available hain
tools = [
    {"type": "function", "function": {
        "name": "search_web",
        "description": "Search the web for current information",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }},
    {"type": "function", "function": {
        "name": "calculate",
        "description": "Evaluate a math expression",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"]
        }
    }},
    {"type": "function", "function": {
        "name": "save_note",
        "description": "Save a note or task to a file",
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"]
        }
    }},
]

# function name ko actual Python function se jodna
available_functions = {
    "search_web": search_web,
    "calculate": calculate,
    "save_note": save_note,
}

def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content  # agent ka final jawab

        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            result = available_functions[fn_name](**fn_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

if __name__ == "__main__":
    query = input("Aap kya poochna chahti hain? ")
    print(run_agent(query))