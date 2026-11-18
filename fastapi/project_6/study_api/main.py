import logging
from os import environ
from pathlib import Path
from time import perf_counter

from fastapi import FastAPI, Request

from .db import lifespan
from .tasks import router


logger = logging.getLogger("uvicorn.error")


def create_app(db_path: Path, token: str):
    app = FastAPI(title="Study Task API", version="1.0", lifespan=lifespan)
    app.state.db_path = db_path
    app.state.token = token

    @app.middleware("http")
    async def measure_request(request: Request, call_next):
        start = perf_counter()
        response = await call_next(request)
        elapsed_ms = (perf_counter() - start) * 1000
        response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.2f}"
        logger.info("%s %s %s %.2fms", request.method, request.url.path, response.status_code, elapsed_ms)
        return response

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(router, prefix="/v1")
    return app


default_db = Path(__file__).resolve().parent.parent / "data" / "tasks.db"
app = create_app(Path(environ.get("TASKS_DB", str(default_db))), environ.get("STUDY_API_TOKEN", ""))
