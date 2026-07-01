# app/main.py — temporary hello version
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(title="Baithak API", version="0.1.0-mvp")

app = FastAPI(title="Baithak API", version="0.1.0-mvp", description=" API ")

# CORS — allow React dev server and production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health")
async def health():
    print("Health endpoint called")
    return {"status": "ok"}