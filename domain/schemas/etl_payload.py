# domain/schemas/etl_payload.py
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class SeguimientoRow(BaseModel):
    fecha_produccion: Optional[str] = None  # dd/mm/yyyy o yyyy-mm-dd
    capitulo: Optional[str] = None
    capitulo_codigo: Optional[str] = None
    certificacion_pendiente: Optional[str | float | int] = None
    resto_produccion: Optional[str | float | int] = None
    observaciones: Optional[str] = None


class PendienteRow(BaseModel):
    fecha_produccion: Optional[str] = None
    capitulo: Optional[str] = None
    capitulo_codigo: Optional[str] = None
    proveedor: Optional[str] = None
    coste_pendiente: Optional[str | float | int] = None
    observaciones: Optional[str] = None


class Header(BaseModel):
    fecha_seguimiento: str = Field(..., description="Inicio!E6")
    empresa: str = Field(..., description="Inicio!E7")
    proyecto: str = Field(..., description="Inicio!B8")


class ExcelPayload(BaseModel):
    header: Header
    seguimiento: List[SeguimientoRow] = Field(default_factory=list)
    pendientes: List[PendienteRow] = Field(default_factory=list)


class RunETLRequest(BaseModel):
    selected_cases: List[str] = Field(default_factory=lambda: ["seguimiento", "pendientes"])
    payload: ExcelPayload


class RunETLResponse(BaseModel):
    ok: bool
    message: str
    rows: dict
