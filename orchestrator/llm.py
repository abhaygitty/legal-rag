import os
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
import config

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")

SYSTEM_PROMPT = """
You are a legal assistant helping answer questions from legal documents.

STRICT RULES:
- Answer ONLY using the provided context
- Do NOT hallucinate
- If answer not present, say: "Answer not found in provided legal documents"
- Cite source and section when available
"""

def count_tokens(text):
    return len(tokenizer.encode(text))

def generate_answer(context: str, query: str):
    print("query: ", query)
    user_prompt = f"""
        Context:
        {context}

        Question:
        {query}
    """
    # print("context: ", context)
    print("context length: ", len(context))

    if count_tokens(context) > config.MAX_CONTEXT_TOKENS:
        raise Exception("Context too large")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=500
    )
    answer = response.choices[0].message.content
    # answer = "generated answer"
    confidence = 0.9
    
    if "Answer not found" in answer:
        confidence = 0.0
    else:
        confidence = 0.95
    return {
        "answer": answer,
        "citations": extract_citations(context),
        "confidence": confidence
    }

def extract_citations(context):
    citations = []
    for line in context.split("\n"):
        if line.startswith("Source:"):
            citations.append(line.replace("Source:", "").strip())
    return list(set(citations))
