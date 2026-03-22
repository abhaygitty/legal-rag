import re

MAX_CHUNK_CHARS = 1500

def chunk_document(doc):
    print("chunking documents...")
    text = doc["text"]
    chunks = []
    for i in range(0, len(text), MAX_CHUNK_CHARS):
        chunk = text[i:i+MAX_CHUNK_CHARS]
        i += MAX_CHUNK_CHARS
        chunks.append({
            "text": chunk,
            "section": "unknown",
            "source": doc["source"]
        })
    
    return chunks

# this prevents huge chunks

# def chunk_document(doc):
#     text = doc["text"]
#     sections = re.split(r'(Section \d+)', text)
#     chunks = []
#     current_section = None

#     for part in sections:
#         if part.startswith("Section"):
#             current_section = part
#         else:
#             chunks.append({
#                 "text": part,
#                 "section": current_section,
#                 "source": doc["source"]
#             })
    
#     return chunks