from fastapi import FastAPI

app = FastAPI(title="Baithak API", version="0.2.0")


@app.get("/health")
async def health():
    return {"status": "ok"}
