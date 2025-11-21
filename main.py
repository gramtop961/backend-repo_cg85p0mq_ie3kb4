import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from datetime import date

from database import db, create_document, get_documents
from schemas import Trainer, Client, Program, Session, Progress

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Private Trainer API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Utility: parse object id safely

def _oid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id format")

# Generic list helper

def _list(collection: str, limit: int = 100):
    return [
        {**{k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}, "_id": str(doc.get("_id"))}
        for doc in get_documents(collection, {}, limit)
    ]

# Trainers

@app.post("/trainers")
def create_trainer(payload: Trainer):
    _id = create_document("trainer", payload)
    return {"_id": _id, **payload.model_dump()}

@app.get("/trainers")
def list_trainers(limit: int = 100):
    return _list("trainer", limit)

# Clients

@app.post("/clients")
def create_client(payload: Client):
    _id = create_document("client", payload)
    return {"_id": _id, **payload.model_dump()}

@app.get("/clients")
def list_clients(limit: int = 100, trainer_id: Optional[str] = None):
    flt = {}
    if trainer_id:
        flt["trainer_id"] = trainer_id
    docs = get_documents("client", flt, limit)
    return [
        {**{k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}, "_id": str(doc.get("_id"))}
        for doc in docs
    ]

# Programs

@app.post("/programs")
def create_program(payload: Program):
    _id = create_document("program", payload)
    return {"_id": _id, **payload.model_dump()}

@app.get("/programs")
def list_programs(limit: int = 100, client_id: Optional[str] = None, trainer_id: Optional[str] = None):
    flt = {}
    if client_id:
        flt["client_id"] = client_id
    if trainer_id:
        flt["trainer_id"] = trainer_id
    docs = get_documents("program", flt, limit)
    return [
        {**{k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}, "_id": str(doc.get("_id"))}
        for doc in docs
    ]

# Sessions

@app.post("/sessions")
def create_session(payload: Session):
    _id = create_document("session", payload)
    return {"_id": _id, **payload.model_dump()}

@app.get("/sessions")
def list_sessions(limit: int = 100, client_id: Optional[str] = None, trainer_id: Optional[str] = None, status: Optional[str] = None):
    flt = {}
    if client_id:
        flt["client_id"] = client_id
    if trainer_id:
        flt["trainer_id"] = trainer_id
    if status:
        flt["status"] = status
    docs = get_documents("session", flt, limit)
    return [
        {**{k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}, "_id": str(doc.get("_id"))}
        for doc in docs
    ]

# Progress

@app.post("/progress")
def create_progress(payload: Progress):
    _id = create_document("progress", payload)
    return {"_id": _id, **payload.model_dump()}

@app.get("/progress")
def list_progress(limit: int = 100, client_id: Optional[str] = None):
    flt = {}
    if client_id:
        flt["client_id"] = client_id
    docs = get_documents("progress", flt, limit)
    return [
        {**{k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}, "_id": str(doc.get("_id"))}
        for doc in docs
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
