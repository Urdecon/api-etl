# application/use_cases/etl_dispatcher.py
from __future__ import annotations

from typing import Dict
from domain.schemas.etl_payload import RunETLRequest


class ETLDispatcher:
    """
    Caso de uso: por ahora valida y contabiliza filas.
    En la siguiente fase conectaremos aquí con tu microservicio ETL real.
    """

    @staticmethod
    def handle(req: RunETLRequest) -> Dict[str, int]:
        selected = [c.strip().lower() for c in req.selected_cases]
        rows: Dict[str, int] = {}
        if "seguimiento" in selected:
            rows["seguimiento"] = len(req.payload.seguimiento)
        if "pendientes" in selected:
            rows["pendientes"] = len(req.payload.pendientes)
        return rows
