from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import nltk
from nltk.tokenize import sent_tokenize

# download once
nltk.download('punkt')

app = FastAPI()

# ✅ CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all frontend requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request model
class InputText(BaseModel):
    text: str
    threshold: float = 0.8

# ✅ Function to remove duplicate sentences
def remove_duplicates(text: str) -> str:
    sentences = sent_tokenize(text)
    unique_sentences = []

    for sentence in sentences:
        if sentence not in unique_sentences:
            unique_sentences.append(sentence)

    return " ".join(unique_sentences)

# ✅ API endpoint
@app.post("/process")
def process_text(data: InputText):
    try:
        cleaned_text = remove_duplicates(data.text)
        return {"cleaned_text": cleaned_text}
    except Exception as e:
        return {"error": str(e)}