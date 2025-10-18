# tests/test_etl.py
from __future__ import annotations

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_etl_run_minimal():
    payload = {
        "selected_cases": ["seguimiento", "pendientes"],
        "payload": {
            "header": {
                "fecha_seguimiento": "18/10/2025",
                "empresa": "RUESMA",
                "proyecto": "PY_002427"
            },
            "seguimiento": [
                {
                    "fecha_produccion": "01/09/2025",
                    "capitulo": "CIM",
                    "capitulo_codigo": "CIM-01",
                    "certificacion_pendiente": "1.234,56",
                    "resto_produccion": "100",
                    "observaciones": "ok"
                }
            ],
            "pendientes": [
                {
                    "fecha_produccion": "02/09/2025",
                    "capitulo": "MUR",
                    "capitulo_codigo": "MUR-10",
                    "proveedor": "",
                    "coste_pendiente": "2.500,00",
                    "observaciones": "por revisar"
                }
            ]
        }
    }
    r = client.post("/v1/etl/run", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["rows"]["seguimiento"] == 1
    assert data["rows"]["pendientes"] == 1
