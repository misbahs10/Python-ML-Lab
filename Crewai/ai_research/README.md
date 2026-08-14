# AI Research Crew

A multi-agent AI research and report generation system built with **CrewAI**.

This project uses multiple specialized AI agents that collaborate to research a topic, analyze the findings, write a professional report, and review the final output.

## 🚀 Project Overview

The **AI Research Crew** follows a sequential multi-agent workflow:

```text
User Topic
    ↓
Researcher Agent
    ↓
Research Task
    ↓
Analyst Agent
    ↓
Analysis Task
    ↓
Writer Agent
    ↓
Writing Task
    ↓
Reviewer Agent
    ↓
Review Task
    ↓
Final Report
```

Instead of asking one AI agent to perform every task, this project divides the work among specialized agents.

## 🤖 Agents

### 1. Researcher Agent

The Researcher is responsible for collecting and organizing information about the requested topic.

Responsibilities:

* Research the topic
* Identify important facts
* Find major developments
* Identify current trends
* Explore real-world applications
* Identify benefits and challenges
* Collect useful sources and references

### 2. Analyst Agent

The Analyst transforms the research into meaningful insights.

Responsibilities:

* Analyze research findings
* Identify key trends
* Find patterns and comparisons
* Identify opportunities
* Identify risks and challenges
* Extract practical insights
* Highlight important conclusions

### 3. Writer Agent

The Writer converts the research and analysis into a professional report.

Responsibilities:

* Create a structured report
* Write an executive summary
* Explain the background and key findings
* Present analytical insights
* Explain applications and benefits
* Discuss challenges
* Provide future trends
* Give recommendations
* Write the conclusion

### 4. Reviewer Agent

The Reviewer performs the final quality check.

Responsibilities:

* Check factual consistency
* Identify missing information
* Detect unsupported claims
* Improve logical flow
* Remove unnecessary repetition
* Improve grammar and readability
* Check formatting
* Improve recommendations
* Produce a polished final report

## 📋 Tasks

The project contains four main tasks.

### Research Task

The Researcher investigates the user-provided topic and produces a structured research document.

### Analysis Task

The Analyst reviews the research and extracts important insights, trends, comparisons, opportunities, risks, and practical implications.

### Writing Task

The Writer combines the research and analysis into a professional Markdown report.

### Review Task

The Reviewer checks and improves the generated report before producing the final version.

## 🔄 Workflow

The project uses a **sequential CrewAI process**.

```text
Research
   ↓
Analysis
   ↓
Writing
   ↓
Review
   ↓
Final Report
```

Each task receives the output of the previous stage, allowing the agents to collaborate as a pipeline.

## ✨ Features

* Multi-agent AI architecture
* Multi-task workflow
* Sequential task execution
* Specialized agent roles
* YAML-based agent configuration
* YAML-based task configuration
* Environment variable support
* Professional report generation
* Final quality-review stage
* Markdown report output
* Optional web research integration

## 🛠️ Technologies Used

* **Python**
* **CrewAI**
* **OpenAI**
* **UV**
* **Tavily** (optional for web research)
* **YAML**
* **Markdown**
* **Git & GitHub**

## 📁 Project Structure

```text
ai_research/
│
├── knowledge/
│
├── src/
│   └── ai_research/
│       │
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       │
│       ├── tools/
│       │
│       ├── __init__.py
│       ├── crew.py
│       └── main.py
│
├── tests/
│
├── .env
├── .gitignore
├── AGENTS.md
├── pyproject.toml
└── README.md
```

## ⚙️ Requirements

Make sure you have:

* Python `>=3.10`
* Python `<3.14`
* UV
* An OpenAI API key

For optional web research:

* Tavily API key

## 📥 Installation

### 1. Clone the repository

```bash
git clone https://github.com/misbahs10/ai_research.git
cd ai_research
```

### 2. Install UV

```bash
pip install uv
```

### 3. Install project dependencies

```bash
uv sync
```

You can also use the CrewAI project installation command:

```bash
crewai install
```

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

`TAVILY_API_KEY` is only required when the Researcher agent is configured to perform web research.

### Security

Never commit your `.env` file to GitHub.

The project should contain:

```text
.env
```

inside `.gitignore`.

Example:

```gitignore
.env
.venv/
__pycache__/
*.pyc
output/
.pytest_cache/
```

## ▶️ Running the Project

From the project root, run:

```bash
uv run run_crew
```

You can also use:

```bash
crewai run
```

The application will ask for a research topic.

Example:

```text
Enter the research topic: Artificial Intelligence in Healthcare
```

The crew will then execute the agents sequentially.

## 📝 Example Workflow

Input:

```text
Artificial Intelligence in Healthcare
```

The system processes the topic like this:

```text
User
 │
 ▼
"Artificial Intelligence in Healthcare"
 │
 ▼
Researcher
 │
 ├── Key concepts
 ├── Trends
 ├── Applications
 ├── Benefits
 └── Challenges
 │
 ▼
Analyst
 │
 ├── Key insights
 ├── Comparisons
 ├── Opportunities
 └── Risks
 │
 ▼
Writer
 │
 └── Professional Report
 │
 ▼
Reviewer
 │
 ├── Fact checking
 ├── Structure review
 ├── Readability
 └── Final improvements
 │
 ▼
Final Report
```

## 📄 Report Structure

The generated report is designed to contain:

```text
1. Title
2. Executive Summary
3. Introduction
4. Background
5. Key Findings
6. Analysis
7. Applications
8. Benefits
9. Challenges
10. Future Trends
11. Recommendations
12. Conclusion
13. Sources
```

## 📤 Output

The final report can be saved as a Markdown file:

```text
output/
└── final_report.md
```

The report can then be converted into other formats such as:

* PDF
* DOCX
* HTML

## 🧩 Configuration

### Agents

Agent roles, goals, and backstories are configured in:

```text
src/ai_research/config/agents.yaml
```

### Tasks

Task descriptions and expected outputs are configured in:

```text
src/ai_research/config/tasks.yaml
```

### Crew Logic

Agent and task orchestration is handled in:

```text
src/ai_research/crew.py
```

### Application Entry Point

The project execution and user input are handled in:

```text
src/ai_research/main.py
```

## 🧠 Why Multi-Agent?

A single AI agent can perform multiple responsibilities, but specialized agents make the workflow easier to organize and extend.

In this project:

```text
Researcher → Research
Analyst    → Analysis
Writer     → Content Generation
Reviewer   → Quality Assurance
```

Each agent has a clearly defined responsibility.

This architecture makes the system easier to maintain, debug, and extend.

## 🔮 Future Improvements

Possible future upgrades include:

* Add a web-search tool
* Add custom CrewAI tools
* Add PDF document ingestion
* Add RAG-based knowledge retrieval
* Add database integration
* Add FastAPI backend
* Add Streamlit frontend
* Generate PDF reports automatically
* Generate DOCX reports
* Add report history
* Add logging and monitoring
* Add citation management
* Add parallel agent execution
* Add human approval before final publishing

## 🎯 Use Cases

This system can be adapted for:

* AI and technology research
* Market research
* Business analysis
* Competitor analysis
* Academic research assistance
* Product research
* Industry trend analysis
* Technical report generation
* Content research
* Research automation

## 🧪 Testing

Tests are stored in:

```text
tests/
```

Run the project's tests using the configured test command:

```bash
uv run test
```

## 📌 Project Scripts

The project provides the following commands:

```bash
uv run run_crew
uv run ai_research
uv run train
uv run replay
uv run test
uv run run_with_trigger
```

The main command for normal execution is:

```bash
uv run run_crew
```

## 📚 Learning Objectives

This project demonstrates practical knowledge of:

* Multi-agent AI systems
* CrewAI framework
* Agent specialization
* Task orchestration
* Sequential workflows
* Prompt engineering
* YAML configuration
* API integration
* Environment variables
* AI-assisted research
* Report automation
* Git and GitHub project management

## 👩‍💻 Author

**Misbah Sajjad**

AI & Data Science
Python | Machine Learning | Data Analytics | CrewAI | n8n | SQL | Power BI

## ⭐ Project Goal

The goal of this project is to demonstrate how multiple specialized AI agents can collaborate to automate a complete research and report-generation workflow.

```text
Research → Analyze → Write → Review → Deliver
```

---

## 📜 License

This project is intended for educational and portfolio purposes.
