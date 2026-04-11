from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
import io

from PyPDF2 import PdfReader
from pptx import Presentation
from docx import Document

app = FastAPI()

#  CORS (VERY IMPORTANT)
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

        # ---------- FILE HANDLING ----------
        if file:
            filename = file.filename.lower()
            content = await file.read()

            # Only allow specific formats
            if not filename.endswith((".pdf", ".ppt", ".pptx", ".docx")):
                return {"result": "Only PDF, PPT, DOCX files allowed"}

            # -------- PDF --------
            if filename.endswith(".pdf"):
                try:
                    reader = PdfReader(io.BytesIO(content))
                    for page in reader.pages:
                        extracted_text += page.extract_text() or ""
                except Exception:
                    return {"result": "Error reading PDF file"}

            # -------- PPT --------
            elif filename.endswith((".ppt", ".pptx")):
                try:
                    prs = Presentation(io.BytesIO(content))
                    for slide in prs.slides:
                        for shape in slide.shapes:
                            if hasattr(shape, "text"):
                                extracted_text += shape.text + " "
                except Exception:
                    return {"result": "Error reading PPT file"}

            # -------- DOCX --------
            elif filename.endswith(".docx"):
                try:
                    doc = Document(io.BytesIO(content))
                    for para in doc.paragraphs:
                        extracted_text += para.text + " "
                except Exception:
                    return {"result": "Error reading DOCX file"}

            text = extracted_text

        # ---------- VALIDATION ----------
        if not text or not text.strip():
            return {"result": "No input provided"}

        # ---------- NLP PROCESS ----------
        from nltk.tokenize import sent_tokenize

        sentences = sent_tokenize(text)
        unique_sentences = list(dict.fromkeys(sentences))

        cleaned_text = " ".join(unique_sentences)

        return {"result": cleaned_text}

    except Exception as e:
        #  prevents crash → avoids CORS error
        return {"result": f"Server error: {str(e)}"}
