import os
import pdfplumber
def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    return text


def load_documents(directory):
    docs = []
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        text = ""
        if(file.endswith(".txt")):
            # text = "Payment of minimum rate of wages says: No employer shall pay to any employee wages less than the minimum rate of wages notified by the appropriate Government"
            text = load_txt(path)
        elif file.endswith(".pdf"):
            # text = "Payment of minimum rate of wages says: No employer shall pay to any employee wages less than the minimum rate of wages notified by the appropriate Government"
            text += load_pdf(path)
        else:
            continue
        
        docs.append({
            "text": text,
            "source": file
        })
    return docs