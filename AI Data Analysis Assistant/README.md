# AI Data Analysis Assistant - HR Employee Attrition

Track A (Explorer) - AI Data Analysis Challenge submission.

## Overview
This project is a simple AI-powered Data Analysis Assistant that:
1. Loads the **HR Employee Attrition** dataset (CSV).
2. Analyzes it using Pandas/NumPy.
3. Answers 3 fixed natural language questions using rule-based logic.
4. Generates a bar chart showing attrition rate by department.
5. Uses the **Groq API** (LLM) to generate a short, human-readable explanation of the findings.

## Dataset
`dataset.csv` - IBM HR Analytics Employee Attrition dataset (1470 rows, 35 columns).
Key columns used: `Attrition`, `Department`, `MonthlyIncome`, `Age`, `JobRole`.

## Project Structure
```
project/
├── main.py              # Orchestrates the full pipeline
├── analysis.py          # Data loading, statistics, question answering
├── visualization.py     # Chart generation
├── ai_explainer.py       # Groq API call for explanation
├── dataset.csv          # Sample dataset
├── requirements.txt
├── README.md
├── .env.example         # Copy to .env and add your Groq API key
└── charts/              # Generated chart is saved here
```

## Setup & Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Add your Groq API key:
   - Copy `.env.example` to `.env`
   - Get a free key from https://console.groq.com and paste it in `.env`:
     ```
     GROQ_API_KEY=your_key_here
     ```
   - If no key is provided, the app still runs and falls back to a rule-based explanation.

3. Run the program:
   ```
   python main.py
   ```

## The 3 Fixed Questions
1. Which department has the highest attrition rate?
2. What is the average monthly income of employees?
3. Which job role has the maximum number of employees?

## Chart
A bar chart (`charts/attrition_by_department.png`) showing the attrition rate (%)
for each department, with proper title, axis labels, and readable colors.

## Notes
- Only one LLM API call is made (in `ai_explainer.py`), as required by the challenge rules.
- Every part of the code is commented and organized into separate modules so it is
  easy to explain during evaluation.