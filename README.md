# Automating Threat Intelligence Extraction with RAG

A Retrieval-Augmented Generation (RAG) project for extracting and answering questions from cybersecurity and threat intelligence reports using open-source language models, vector search, and PDF ingestion.

## Overview

This project ingests PDF-based threat intelligence reports, splits them into chunks, converts them into embeddings, stores them in Qdrant, and answers user questions by retrieving the most relevant context and passing it to a local open-source LLM.

## Features

- PDF ingestion and chunking
- Embedding generation using Sentence Transformers
- Vector storage and retrieval using Qdrant
- Local question answering using Qwen
- CLI-based ingestion and querying
- Modular project structure for future FastAPI/API integration

## Tech Stack

- Python
- Qdrant
- Sentence Transformers
- Hugging Face Transformers
- Qwen open-source LLM
- LangChain text splitters
- Docker

## Project Structure

```text
Automating-Threat-Intelliegence-Extraction-with-RAG/
│
├── app/
│   ├── __init__.py
│   ├── llm.py
│   ├── embeddings.py
│   ├── ingest.py
│   ├── rag.py
│   └── vectordb.py
│
├── scripts/
│   ├── __init__.py
│   ├── run_ingest.py
│   └── run_query.py
│
├── data/
├── tests/
├── requirements.txt
└── README.md