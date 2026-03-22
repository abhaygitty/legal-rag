from sentence_transformers import CrossEncoder
import config

model = CrossEncoder(config.RERANK_MODEL)

def rerank(query, docs):
    pairs = [(query, d[0]) for d in docs]
    scores = model.predict(pairs)
    reranked = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # reranked_docs = [r[0] for r in reranked]

    # return reranked_docs[:config.MAX_CONTEXT_CHUNKS] # reduces the chunks returned to a maximum chunk count limit

    return [doc for doc, score in reranked]