# Cost-Efficient RAG Application

A Retrieval-Augmented Generation (RAG) application designed to answer questions from PDF, HTML, and Markdown documents using a persistent, low-cost vector store.

**Project status:** Phase 1 — Foundation and API setup.

## Objectives

- Ingest PDF, HTML, and Markdown documents.
- Generate embeddings and store them in ChromaDB.
- Retrieve relevant document chunks using semantic search.
- Generate grounded answers with source citations.
- Evaluate retrieval quality, answer quality, latency, and cost.
- Provide a reproducible, Dockerized backend service.

## Technology Stack

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- LLM provider for answer generation
- Pytest
- Docker

## Project Structure

```text
cost-efficient-rag/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── config.py
├── tests/
│   └── test_health.py
├── storage/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/anurag-jpg/cost-efficient-rag.git
cd cost-efficient-rag
```

### 2. Create a virtual environment

Windows:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and review the settings.

Never commit `.env` or real API credentials.

### 5. Start the API

```bash
python -m uvicorn app.main:app --reload
```

Health endpoint: `http://127.0.0.1:8000/health`

API documentation: `http://127.0.0.1:8000/docs`

### 6. Run tests

```bash
python -m pytest -v
```

## Evaluation Plan

The completed application will be evaluated using a fixed question dataset.

### Retrieval metrics
- Recall@k
- Hit Rate@k
- Mean Reciprocal Rank (MRR)
- nDCG@k
- Context precision

### Answer metrics
- Faithfulness / groundedness
- Answer relevance
- Exact Match and F1 where appropriate

### Performance and cost
- Retrieval and end-to-end p50/p95 latency
- Token usage
- Monthly cost estimates for 100K, 1M, and 10M vectors
- Comparison with a managed vector database

## Current Status

- [x] Initial project structure
- [x] Environment configuration
- [x] FastAPI health endpoint
- [x] Initial automated test
- [ ] PDF, HTML, and Markdown ingestion
- [ ] Idempotent chunk storage
- [ ] Embedding generation and ChromaDB integration
- [ ] Semantic retrieval and grounded answers
- [ ] Evaluation harness and cost benchmarks
- [ ] Docker setup

## Design Trade-offs

ChromaDB is the initial choice because it supports persistent local storage and avoids the need for an always-on managed vector database during development.

Actual cost savings, retrieval quality, and scaling limits will be established through measurements rather than assumed in advance.

## License

No license has been selected yet.