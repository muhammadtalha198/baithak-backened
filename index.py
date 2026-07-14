from fastapi import FastAPI
from fastapi.responses import JSONResponse


def _build_app() -> FastAPI:
    try:
        from app.server import app as application

        return application
    except Exception as exc:
        fallback = FastAPI(title="Baithak API", version="0.2.0-debug")

        @fallback.get("/health")
        async def health():
            return JSONResponse(
                status_code=503,
                content={"status": "error", "detail": str(exc)},
            )

        @fallback.get("/{full_path:path}")
        async def catch_all(full_path: str):
            return JSONResponse(
                status_code=503,
                content={"status": "error", "detail": str(exc), "path": full_path},
            )

        return fallback


app = _build_app()
