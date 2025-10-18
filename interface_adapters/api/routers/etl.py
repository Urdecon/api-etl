# interface_adapters/api/routers/etl.py
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from domain.schemas.etl_payload import RunETLRequest, RunETLResponse
from application.use_cases.etl_dispatcher import ETLDispatcher

router = APIRouter(prefix="/etl", tags=["etl"])


@router.post("/run", response_model=RunETLResponse)
def run_etl(req: RunETLRequest):
    selected = [c.strip().lower() for c in req.selected_cases]
    if not selected:
        raise HTTPException(status_code=400, detail="selected_cases vacío.")

    rows = ETLDispatcher.handle(req)
    if not rows:
        raise HTTPException(status_code=400, detail="Ningún caso válido en selected_cases.")

    return RunETLResponse(ok=True, message="Solicitud aceptada.", rows=rows)
