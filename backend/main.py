from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
def process_text(data: dict):
    text = data.get("text", "")

    # Split sentences correctly
    sentences = [s.strip() for s in text.split(".") if s.strip()]

    # Remove duplicates
    unique = list(dict.fromkeys(sentences))

    # Join with proper spacing
    cleaned = ". ".join(unique) + "."

    return {"result": cleaned}
