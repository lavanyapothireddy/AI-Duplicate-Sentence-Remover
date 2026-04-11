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

def get_text_from_file(file: UploadFile):
    name = file.filename.lower()
    text = ""
    try:
        content = file.file.read()
        if name.endswith('.pdf'):
            pdf = PdfReader(io.BytesIO(content))
            text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif name.endswith('.docx'):
            doc = Document(io.BytesIO(content))
            text = " ".join([p.text for p in doc.paragraphs])
        elif name.endswith(('.pptx', '.ppt')):
            prs = Presentation(io.BytesIO(content))
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + " "
    except Exception as e:
        print(f"Error reading file: {e}")
    return text

@app.post("/process")
async def process_text(text: str = Form(None), file: UploadFile = File(None)):
    raw_input = ""
    
    if file:
        raw_input = get_text_from_file(file)
    elif text:
        raw_input = text

    if not raw_input.strip():
        return {"result": "No content to process."}

    # Split by common sentence endings (. ! ?)
    # This handles "hi.hi" correctly
    sentences = re.split(r'(?<=[.!?])\s*', raw_input.strip())
    
    seen = set()
    unique = []
    for s in sentences:
        clean = s.strip()
        if clean and clean.lower() not in seen:
            unique.append(clean)
            seen.add(clean.lower())

    return {"result": " ".join(unique)}
