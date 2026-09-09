# LedgerLens v2 — Financial Intelligence Platform

The production version of LedgerLens. A RAG-powered financial analytics platform built on SEC 10-K filings.

## Features

- Natural language Q&A grounded in real SEC documents
- 4,765 vector chunks indexed with FAISS
- Groq LLM for structured responses with citations
- Financial Health Score across Profitability, Growth, Safety, Cash
- Interactive Plotly charts
- Company comparison with radar visualization
- AI-generated executive reports

## Modules

| Module | Description |
|---|---|
| `dashboard/app.py` | Main Streamlit application |
| `rag/` | Document loading, chunking, embeddings, retrieval |
| `llm/` | Groq API handler and prompt templates |
| `analytics/` | Financial engine, ratios, health score |
| `utils/` | Response parser and formatter |
| `data/` | PDFs, extracted text, processed CSV |

## Stack

Python · LangChain · FAISS · HuggingFace · Groq · PyMuPDF · Streamlit · Plotly · Pandas