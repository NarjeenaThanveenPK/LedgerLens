# LedgerLens v1 — Rule-Based Financial Assistant

Developed as part of the BCG GenAI Job Simulation on Forage.

A rule-based financial chatbot that analyzes SEC 10-K data 
for Apple, Microsoft, and Tesla (2023–2025).

## Files
- `chatbot.py` — rule-based chatbot with keyword matching
- `analysis.ipynb` — financial data analysis notebook
- `financial_data.csv` — structured dataset from SEC 10-K filings

## How to run
```bash
pip install -r requirements.txt
python chatbot.py
```

## How it works
- Financial data manually extracted from SEC 10-K filings
- Keyword matching identifies user intent
- Pandas handles dynamic calculations
- Answers explained in plain non-financial language

## Supported questions
- Which company had the highest revenue?
- Which company had the highest net income?
- How did Microsoft's revenue change?
- How did Tesla's profit change?
- Compare Apple and Microsoft
- Which company appears financially strongest?
- What is operating cash flow?

## Stack
Python, Pandas

## Limitations
- Predefined questions only
- No NLP or semantic understanding
- No LLM integration

## This is Version 1. Version 2 is being engineered above.