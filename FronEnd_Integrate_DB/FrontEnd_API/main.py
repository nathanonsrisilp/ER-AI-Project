from fastapi import FastAPI, UploadFile, File
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from openai import OpenAI

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "er_helper")

client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["dispatches"]

class Dispatch(BaseModel):
    Timestamp: str
    Address: str
    Lat: float
    Lon: float
    Type: str
    Severity: str
    Transcript: str
    Response: Optional[str] = None

@app.get("/dispatches", response_model=List[Dispatch])
def get_dispatches():
    data = list(collection.find({}, {"_id": 0}))
    return data

@app.post("/dispatches", response_model=Dispatch)
def create_dispatch(dispatch: Dispatch):
    collection.insert_one(dispatch.dict())
    return dispatch

# Audio
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        with open(temp_file_path, "rb") as audio_file:
            transcript = client_openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        result_text = transcript.text
    except Exception as e:
        result_text = f"Error transcribing: {str(e)}"
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {"transcript": result_text}