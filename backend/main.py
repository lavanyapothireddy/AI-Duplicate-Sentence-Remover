from fastapi import FastAPI, Form, File, UploadFile
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
    return {"message": "API running"}

@app.post("/process")
async def process(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    if file:
        return {"result": f"Received file: {file.filename}"}

    if text:
        return {"result": text}

    return {"result": "No input provided"}
