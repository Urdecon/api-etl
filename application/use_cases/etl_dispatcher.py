# application/use_cases/etl_dispatcher.py
from __future__ import annotations
import json, os, shlex, subprocess
from typing import Dict, Any, List
from fastapi import HTTPException
from domain.schemas.etl_payload import RunETLRequest
from config.settings import Settings

def _split_cmd_win(cmd: str) -> List[str]:
    return shlex.split(cmd, posix=False)

def _augment_env_for_venv(py_exe: str, base_env: dict) -> dict:
    env = dict(base_env)
    scripts_dir = os.path.dirname(py_exe)
    venv_dir = os.path.dirname(scripts_dir)
    env["VIRTUAL_ENV"] = venv_dir
    env["PYTHONIOENCODING"] = "utf-8"
    env["PATH"] = scripts_dir + os.pathsep + env.get("PATH", "")
    return env

def _maybe_force_venv_python(parts: List[str], workdir: str) -> List[str]:
    """Si el primer token es 'python' o 'py', sustituye por el python del venv del ETL."""
    if not parts:
        return parts
    first = parts[0].strip('"').lower()
    if first in ("python", "python.exe", "py", "py.exe"):
        venv_py = os.path.join(workdir, ".venv", "Scripts", "python.exe")
        if os.path.exists(venv_py):
            parts[0] = venv_py
    return parts

class ETLDispatcher:
    @staticmethod
    def handle(req: RunETLRequest) -> Dict[str, int]:
        settings = Settings()
        if not settings.ETL_WORKDIR:
            raise HTTPException(status_code=500, detail="ETL_WORKDIR no está configurado.")

        in_payload: Dict[str, Any] = json.loads(req.model_dump_json())

        # Construir comando
        parts = _split_cmd_win(settings.ETL_RUN_CMD)
        parts = _maybe_force_venv_python(parts, settings.ETL_WORKDIR)

        if not parts:
            raise HTTPException(status_code=500, detail="ETL_RUN_CMD vacío o inválido.")
        py_exe = parts[0].strip('"')
        args = parts[1:]

        env = _augment_env_for_venv(py_exe, os.environ)

        # Preflight: importa yaml con ese exe/env/cwd
        pre = subprocess.run(
            [py_exe, "-c", "import sys,yaml; print(sys.executable); print('YAML', yaml.__version__)"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=settings.ETL_WORKDIR, env=env, check=False,
        )
        if pre.returncode != 0:
            raise HTTPException(status_code=500, detail={
                "message": "Preflight PyYAML falló",
                "stderr": pre.stderr.decode("utf-8", errors="replace")[-4000:],
                "stdout": pre.stdout.decode("utf-8", errors="replace")[-4000:],
                "python": py_exe,
                "cwd": settings.ETL_WORKDIR,
                "cmd": settings.ETL_RUN_CMD,
            })

        # Ejecutar runner
        completed = subprocess.run(
            [py_exe, *args],
            input=json.dumps(in_payload).encode("utf-8"),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=settings.ETL_WORKDIR, env=env, check=False,
        )

        if completed.returncode != 0:
            raise HTTPException(status_code=500, detail={
                "message": f"Runner ETL exit code {completed.returncode}",
                "stderr": completed.stderr.decode("utf-8", errors="replace")[-4000:],
                "stdout": completed.stdout.decode("utf-8", errors="replace")[-4000:],
                "python": py_exe,
                "cwd": settings.ETL_WORKDIR,
                "cmd": settings.ETL_RUN_CMD,
            })

        # Parsear salida
        try:
            out = json.loads(completed.stdout.decode("utf-8"))
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail={
                "message": "Salida del runner no es JSON",
                "stdout_tail": completed.stdout.decode("utf-8", errors="replace")[-4000:],
                "stderr_tail": completed.stderr.decode("utf-8", errors="replace")[-4000:],
            })

        if not out.get("ok"):
            raise HTTPException(status_code=500, detail=out)

        return out.get("rows", {})
