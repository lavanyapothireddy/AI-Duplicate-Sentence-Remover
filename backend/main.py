from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

app = FastAPI()

# ✅ Enable CORS (IMPORTANT for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (you can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route (fixes "Not Found")
@app.get("/")
def home():
    return {"message": "AI Duplicate Sentence Remover API is running 🚀"}

# Input model
class InputText(BaseModel):
    text: str
    threshold: float = 0.8

# ✅ Main API
@app.post("/process")
def process_text(data: InputText):
    try:
        text = data.text
        threshold = data.threshold

        # Split into sentences
        sentences = sent_tokenize(text)

        if len(sentences) <= 1:
            return {"result": text}

        # Convert sentences into vectors
        vectorizer = TfidfVectorizer().fit_transform(sentences)
        vectors = vectorizer.toarray()

        # Compute similarity matrix
        similarity_matrix = cosine_similarity(vectors)

        # Remove duplicates
        unique_sentences = []
        used = set()

        for i in range(len(sentences)):
            if i in used:
                continue
            unique_sentences.append(sentences[i])

            for j in range(i + 1, len(sentences)):
                if similarity_matrix[i][j] > threshold:
                    used.add(j)

        result_text = " ".join(unique_sentences)

        return {"result": result_text}

    except Exception as e:
        return {"error": str(e)}
