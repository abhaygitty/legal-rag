POSTGRES = {
    "host": "localhost",
    "port": 5433,
    "dbname": "legal_rag",
    "user": "legal",
    "password": "legal"
}

OPENSEARCH_URL = "http://localhost:9200"

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
RERANK_MODEL =  "BAAI/bge-reranker-large"

TOP_K = 10
TOP_K_VECTOR = 20
TOP_K_BM25 = 20
TOP_K_RERANK = 10
MAX_CONTEXT_CHUNKS = 6   # critical
MAX_CONTEXT_TOKENS = 6000