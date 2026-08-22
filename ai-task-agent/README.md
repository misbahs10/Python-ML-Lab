# AI Task Agent

A Python-based AI agent that answers user questions and performs tasks by dynamically selecting and calling tools — including web search, calculations, and note-saving.

## Overview

Unlike a standard chatbot that only generates text, this agent can reason about what a request needs, decide which tool (if any) to use, execute that tool, and return an accurate final answer — built using OpenAI-style function calling on top of the Groq API.

## How It Works

1. The user submits a query
2. The LLM analyzes the request and decides whether a tool call is needed
3. If needed, the appropriate tool is executed and its result is returned to the LLM
4. The LLM uses that result to generate a final, natural-language response

This follows a **Reasoning → Action → Observation** loop, repeating until the agent has enough information to answer.

## Tools

| Tool | Description |
|---|---|
| `calculate` | Evaluates mathematical expressions |
| `search_web` | Searches the web for current information via the Tavily API |
| `save_note` | Saves a note or task to a local file (`notes.txt`) |

## Tech Stack

- **Python**
- **Groq API** — LLM inference (`openai/gpt-oss-20b`)
- **Tavily API** — real-time web search
- **python-dotenv** — environment variable management

## Project Structure

```
ai-task-agent/
├── agent/
│   └── main.py            # Core agent loop
├── tools/
│   ├── calculator_tool.py
│   ├── search_tool.py
│   └── task_tool.py
├── .env                    # API keys (not committed)
├── .gitignore
└── requirements.txt
```

## Setup

1. Clone the repository and navigate to the `ai-task-agent` folder

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   GROQ_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   ```

## Usage

```bash
python agent/main.py
```

The agent will prompt for a query and respond, calling tools automatically as needed.

## Example Queries

| Query | Tool Triggered |
|---|---|
| `What is 25 * 17?` | `calculate` |
| `What's the weather in Karachi today?` | `search_web` |
| `Save this note: meeting tomorrow at 5 PM` | `save_note` |

## Future Improvements

- Add conversation memory across multiple turns
- Expand toolset (e.g., email sending, file summarization)
- Wrap the agent in a FastAPI endpoint for external access

## Author

Misbah Sajjad — AI & Data Science enthusiast, building practical AI agent and machine learning projects.