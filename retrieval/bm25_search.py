from opensearchpy import OpenSearch
import config

client = OpenSearch(config.OPENSEARCH_URL)

def search(query):
    res = client.search(
        index="legal_chunks",
        body={
            "query": {
                "match": {
                    "text": query
                }
            },
            "size": config.TOP_K
        }
    )
    
    return res["hits"]["hits"]