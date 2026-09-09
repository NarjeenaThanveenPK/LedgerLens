# LedgerLens — Financial Intelligence Platform

> An AI-powered platform that analyzes SEC 10-K annual filings for Apple, Microsoft, and Tesla using Retrieval-Augmented Generation (RAG), financial analytics, and large language models.

## Live Demo

🔗 [Coming Soon — Deploying to Streamlit Community Cloud]

## What it does

- Ask natural language questions about company financials in plain English
- Get structured answers grounded in actual SEC 10-K filings with citations
- Interactive financial charts — revenue, profit, cash flow, margins
- Side-by-side company comparison with radar charts
- Financial Health Score computed from real ratios
- Executive report generation per company

## Architecture

```text
User Query
    ↓
Streamlit Interface
    ↓
Query Processing
    ↓                    ↓
Financial Engine         RAG Pipeline
Pandas · Ratios          LangChain · FAISS
    ↓                    ↓
        Groq LLM
           ↓
Summary · Metrics · Charts · Sources
```

## Tech Stack

| Layer | Technology |
|---|---|
| Interface | Streamlit |
| RAG Pipeline | LangChain · FAISS |
| Embeddings | HuggingFace sentence-transformers |
| LLM | Groq API |
| PDF Parsing | PyMuPDF |
| Analytics | Python · Pandas |
| Charts | Plotly |

## Data Coverage

- **Companies:** Apple (AAPL) · Microsoft (MSFT) · Tesla (TSLA)
- **Documents:** SEC 10-K Annual Filings
- **Years:** FY 2023 · 2024 · 2025
- **Vector chunks indexed:** 4,765

## Project Structure

```text
LedgerLens/
├── v1_rule_based/        ← BCG simulation prototype
│   ├── chatbot.py
│   ├── financial_data.csv
│   ├── analysis.ipynb
│   └── README.md
│
├── v2_platform/          ← Full RAG platform
│   ├── analytics/        ← Financial engine and health score
│   ├── dashboard/        ← Streamlit app
│   ├── data/             ← PDFs, processed text, CSV
│   ├── llm/              ← Groq handler and prompts
│   ├── rag/              ← LangChain, FAISS, embeddings
│   ├── utils/            ← Response builder
│   └── requirements.txt
│
├── docs/
├── screenshots/
├── README.md
└── ROADMAP.md
```

## Version History

**v1 — Rule-Based Assistant**

Developed as part of the BCG GenAI Job Simulation on Forage. Keyword matching, Pandas analytics, predefined financial queries.

**v2 — Financial Intelligence Platform**

Full RAG pipeline with semantic search over 9 SEC 10-K reports, Groq LLM for grounded answer generation, interactive Streamlit dashboard, financial health scoring, and company comparison.

## Local Setup

```bash
git clone https://github.com/NarjeenaThanveenPK/LedgerLens.git
cd LedgerLens/v2_platform
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in `v2_platform/`:

```env
GROQ_API_KEY=your_key_here
```

Run:

```bash
streamlit run dashboard/app.py
```

## Author

Narjeena Thanveen P K — [LinkedIn](https://www.linkedin.com/in/narjeena-thanveen-p-k-454bb0215/) · [GitHub](https://github.com/NarjeenaThanveenPK)
