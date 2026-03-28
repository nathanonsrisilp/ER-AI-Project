from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "er_helper")

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