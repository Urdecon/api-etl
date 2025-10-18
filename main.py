# main.py
from __future__ import annotations

import logging
import uvicorn
from fastapi import FastAPI

from config.settings import Settings
from interface_adapters.api.routers.etl import router as etl_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def create_app() -> FastAPI:
    app = FastAPI(title="ETL Excel API", version="1.0.0")

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    # Rutas de negocio (v1)
    app.include_router(etl_router, prefix="/v1")
    return app


app = create_app()

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
