from ingestion.loader import load_documents
from ingestion.chunker import chunk_document
from ingestion.embedder import embed
from ingestion.indexer import index_chunk

docs = load_documents("legal_docs2")

for doc in docs:
    chunks = chunk_document(doc)

    print("embedding text...")
    print("and...")
    print("indexing chunks...")
    for chunk in chunks:
        emb = embed(chunk["text"])
        index_chunk(chunk, emb)