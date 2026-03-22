# Legal Hybrid RAG System — Runbook

This document describes how to completely tear down and bring up the Legal Hybrid Retrieval-Augmented Generation (RAG) system from scratch.

---

# Architecture Overview

Components:

* PostgreSQL + pgvector → vector storage
* OpenSearch → BM25 keyword search
* FastAPI → API server
* Ingestion pipeline → document indexing
* OpenAI → answer generation
* Hybrid retrieval → vector + BM25 + reranker

---

# Prerequisites

Install:

* Docker Desktop
* Python 3.9+
* pip
* virtualenv

Verify:

```bash
docker --version
python3 --version
```

---

# Project Structure

```
legal-rag/
│
├── api/
├── ingestion/
├── retrieval/
├── orchestrator/
├── scripts/
├── legal_docs/
├── docker-compose.yml
├── config.py
├── requirements.txt
└── .env
```

---

# Environment Setup

Create `.env` file in project root:

```
OPENAI_API_KEY=your-api-key
```

---

# Full Teardown (Clean Reset)

Stops containers and deletes database volume.

```bash
docker compose down -v

docker rm -f legal-rag-postgres 2>/dev/null || true
docker rm -f legal-rag-opensearch 2>/dev/null || true

docker volume prune -f
```

Verify clean state:

```bash
docker ps -a
docker volume ls
```

---

# Start Infrastructure

Start PostgreSQL and OpenSearch:

```bash
docker compose up -d
```

Verify containers:

```bash
docker ps
```

Expected:

```
legal-rag-postgres
legal-rag-opensearch
```

---

# Verify Database Connectivity

Connect to Postgres:

```bash
psql -h localhost -p 5433 -U legal -d legal_rag
```

Password:

```
legal
```

Verify tables:

```sql
\dt
```

Verify pgvector extension:

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

Exit:

```sql
\q
```

---

# Setup Python Environment

Create virtual environment:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Ingest Documents

Place legal documents inside:

```
legal_docs/
```

Supported formats:

```
.pdf
.txt
```

Run ingestion:

```bash
python -m scripts.ingest_directory
```

Expected output:

```
Loading documents...
Chunking...
Embedding...
Indexing...
Done.
```

---

# Verify Data in Database

Connect:

```bash
psql -h localhost -p 5433 -U legal -d legal_rag
```

Check record count:

```sql
SELECT COUNT(*) FROM legal_chunks;
```

View sample records:

```sql
SELECT source, section FROM legal_chunks LIMIT 5;
```

Exit:

```sql
\q
```

---

# Start API Server

Activate virtual environment:

```bash
source venv/bin/activate
```

Start FastAPI server:

```bash
uvicorn api.main:app --reload
```

Expected output:

```
Uvicorn running on http://127.0.0.1:8000
```

---

# Test API Endpoint

Run:

```bash
curl -X POST "http://127.0.0.1:8000/query?q=What%20is%20minimum%20wage?"
```

Expected response:

```json
{
  "answer": "...",
  "citations": ["code_on_wages_2019.pdf"],
  "confidence": 0.95
}
```

---

# Verify OpenSearch

Check OpenSearch status:

```bash
curl http://localhost:9200
```

Verify index exists:

```bash
curl http://localhost:9200/legal_chunks/_count
```

---

# Verify Vector Index Performance

Connect to database:

```bash
psql -h localhost -p 5433 -U legal -d legal_rag
```

Run:

```sql
EXPLAIN ANALYZE
SELECT text
FROM legal_chunks
ORDER BY embedding <-> '[0,0,0]'::vector
LIMIT 5;
```

Exit:

```sql
\q
```

---

# Restart API Server (if needed)

Stop:

```
CTRL+C
```

Restart:

```bash
uvicorn api.main:app --reload
```

---

# Stop Everything

Stop API server:

```
CTRL+C
```

Stop infrastructure:

```bash
docker compose down
```

---

# Full Clean Restart Checklist

Run in order:

```
docker compose down -v
docker compose up -d

source venv/bin/activate
python -m scripts.ingest_directory

uvicorn api.main:app --reload

curl -X POST "http://127.0.0.1:8000/query?q=test"
```

---

# Troubleshooting

## Check DB connection

```bash
psql -h localhost -p 5433 -U legal -d legal_rag
```

## Check OpenSearch

```bash
curl http://localhost:9200
```

## Check API logs

View uvicorn terminal.

---

# Production Notes

Recommended limits:

```
MAX_CONTEXT_CHUNKS = 6
MAX_CONTEXT_TOKENS = 6000
```

Recommended model:

```
gpt-4o-mini
```

---

# System is now fully operational.
