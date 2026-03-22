import tiktoken
import config

tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")

def count_tokens(text):
    return len(tokenizer.encode(text))

def build_context(results):
    context_parts = []

    total_tokens = 0

    for text, section, source in results:
        chunk = f"""
        Source: {source}
        Section: {section}
        {text}
        """  
        chunk_tokens = count_tokens(chunk)  
        
        if(total_tokens + chunk_tokens > config.MAX_CONTEXT_TOKENS):
            break

        context_parts.append(chunk)
        total_tokens += chunk_tokens
    
    return "\n---\n".join(context_parts)
    
    
    # context = ""

    # for r in results:
    #     context += f"""
    #     Source: {r[1]}
    #     Text: {r[0]}

    #     """
    # return context