from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import re
import io
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADD THIS: This stops the "detail: Not Found" error at the main link
@app.get("/")
async def home():
    return {"message": "API is Online and Running!"}

@app.post("/read-file")
async def read_file_endpoint(file: UploadFile = File(...)):
    try:
        name = file.filename.lower()
        content = await file.read()
        text = ""

        if name.endswith('.pdf'):
            pdf = PdfReader(io.BytesIO(content))
            text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif name.endswith('.docx'):
            doc = Document(io.BytesIO(content))
            text = " ".join([p.text for p in doc.paragraphs])
        else:
            text = content.decode("utf-8", errors="ignore")

        return {"text": text.strip() if text.strip() else "No text found."}
    except Exception as e:
        return {"text": f"Error: {str(e)}"}

@app.post("/process")
async def process_endpoint(text: str = Form(None)):
    if not text: return {"result": "Empty"}
    sentences = re.split(r'(?<=[.!?])\s*', text.strip())
    unique, seen = [], set()
    for s in sentences:
        if s.strip().lower() not in seen:
            unique.append(s.strip())
            seen.add(s.strip().lower())
    return {"result": " ".join(unique)}
