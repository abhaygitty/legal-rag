import psycopg2
from opensearchpy import OpenSearch
import config

conn = psycopg2.connect(**config.POSTGRES)
os_client = OpenSearch(config.OPENSEARCH_URL)

def index_chunk(chunk, embedding):
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO legal_chunks
                (text, embedding, section, source)
                VALUES (%s, %s, %s, %s)
                """, (
                    chunk["text"],
                    embedding,
                    chunk["section"],
                    chunk["source"]
                ))
    
    conn.commit()

    os_client.index(
        index="legal_chunks",
        body={
            "text": chunk["text"],
            "section": chunk["section"],
            "source": chunk["source"]
        }
    )