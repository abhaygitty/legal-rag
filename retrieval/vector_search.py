import psycopg2
import config

conn = psycopg2.connect(**config.POSTGRES)

def search(query_embedding):
    cur = conn.cursor()
    conn.rollback()   # <-- add this line

    cur.execute("""
        SELECT text, section, source,
        embedding <-> %s::vector AS distance
        FROM legal_chunks
        ORDER BY distance
        LIMIT %s
""", (query_embedding, config.TOP_K))


    vector_search_result = cur.fetchall()
    # print("vector_search_result: ", vector_search_result)
    return vector_search_result