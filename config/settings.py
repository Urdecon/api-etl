# config/settings.py
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuración de la API (independiente del ETL)."""
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8088"))
    ENV: str = os.getenv("ENV", "dev")

    # ── Comando para invocar el runner del ETL como proceso ──
    # Ejemplo en Windows:
    #   ETL_RUN_CMD=python -m interface_adapters.controllers.etl_api_entry
    #   ETL_WORKDIR=C:\Users\pgris\PycharmProjects\snapshot_bc
    ETL_RUN_CMD: str = os.getenv("ETL_RUN_CMD", "python -m interface_adapters.controllers.etl_api_entry")
    ETL_WORKDIR: str = os.getenv("ETL_WORKDIR", "")
