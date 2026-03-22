def hybrid_search(vector_results, bm25_results):
    scores = {}
    metadata = {}

    k = 60

    for rank, row in enumerate(vector_results):
        text, section, source, distance = row
        key = (text, section, source)
        scores[key] = scores.get(key, 0) + 1/(k+rank)
        metadata[key] = key
    
    for rank, r in enumerate(bm25_results):
        text = r["_source"]["text"]
        section = r["_source"].get("section", "")
        source = r["_source"].get("source", "")
        key = (text, section, source)
        scores[key] = scores.get(key, 0) + 1/(k+rank)
        metadata[key] = key
    

    # for rank, r in enumerate(vector_results):
    #     scores[r[0]] = scores.get(r[0], 0) + 1/(k+rank)
    
    # for rank, r in enumerate(bm25_results):
    #     text = r["_source"]["text"]
    #     scores[text] = scores.get(text, 0) + 1/(k+rank)
    
    sorted_results = sorted(scores.items(),
                            key=lambda x: x[1],
                            reverse=True)
    
    return [metadata[k] for k, _ in sorted_results]

