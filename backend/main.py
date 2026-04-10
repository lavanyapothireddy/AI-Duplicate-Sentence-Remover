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
    
    sentences = list(dict.fromkeys(text.split(".")))
    cleaned = ".".join([s.strip() for s in sentences if s.strip()])

    return {"result": cleaned}
