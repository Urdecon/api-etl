# config/settings.py
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuración de la API (independiente del ETL)."""
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    ENV: str = os.getenv("ENV", "dev")
