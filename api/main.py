from fastapi import FastAPI

from ingestion.embedder import embed

from retrieval.vector_search import search as vector_search
from retrieval.bm25_search import search as bm25_search

from retrieval.hybrid import hybrid_search
from retrieval.reranker import rerank

from orchestrator.context_builder import build_context
from orchestrator.llm import generate_answer

app = FastAPI()

@app.post("/query")
def query(q: str):
    # q = "What does Payment of minimum rate of wages say in the Wage Code 2019?"
    q = "What are the components of minimum wages?"
    query_embedding = embed(q)
    print("query_embedding length: ", len(query_embedding))
    vector_results = vector_search(query_embedding)
    print("vector_results length: ", len(vector_results))
    # print("vector_results[0]: ", vector_results[0])
    bm25_results = bm25_search(q)
    print("bm25_results length: ", len(bm25_results))
    # print("bm25 result[0] length: ", len(bm25_results[0]))
    hybrid = hybrid_search(vector_results, bm25_results)
    print("hybrid length: ", len(hybrid))
    reranked = rerank(q, hybrid)
    print("reranked length: ", len(reranked))
    context = build_context(reranked)
    # print("context length: ", len(context))

    return generate_answer(context, q)