from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import nltk
import io

from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader
from pptx import Presentation
from docx import Document
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')
app = FastAPI()
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "API is running"}
@app.post("/process")
async def process_text(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        extracted_text = ""
        # ---------- 1. FILE HANDLING ----------
        if file:
            filename = file.filename.lower()
            content = await file.read()
            if not filename.endswith((".pdf", ".ppt", ".pptx", ".docx")):
                return {"result": "Unsupported file format. Use PDF, PPT, or DOCX."}
            # Extracting from PDF
            if filename.endswith(".pdf"):
                reader = PdfReader(io.BytesIO(content))
                for page in reader.pages:
                    extracted_text += (page.extract_text() or "") + " "
            # Extracting from PPT
            elif filename.endswith((".ppt", ".pptx")):
                prs = Presentation(io.BytesIO(content))
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            extracted_text += shape.text + " "
            # Extracting from DOCX
            elif filename.endswith(".docx"):
                doc = Document(io.BytesIO(content))
                for para in doc.paragraphs:
                    extracted_text += para.text + " "
            text = extracted_text
        # ---------- 2. VALIDATION ----------
        if not text or not text.strip():
            return {"result": "No text content found to process."}
        # ---------- 3. NLP DEDUPLICATION ----------
        # Tokenize text into individual sentences
        raw_sentences = sent_tokenize(text)
        # Deduplication logic:
        # 1. Strip leading/trailing whitespace
        # 2. Filter out empty strings
        # 3. Use dict.fromkeys to remove duplicates while keeping original order
        seen = set()
        unique_sentences = []
        for s in raw_sentences:
            clean_s = s.strip()
            if clean_s and clean_s not in seen:
                unique_sentences.append(clean_s)
                seen.add(clean_s)
        cleaned_result = " ".join(unique_sentences)
        return {"result": cleaned_result}
    except Exception as e:
        # Return error message to frontend instead of crashing
        return {"result": f"Server error: {str(e)}"}
