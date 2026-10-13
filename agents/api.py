"""
FastAPI REST API Server for Sphincs Stateless Hash Sign.
"""
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import os
import hmac
from .base import AuditLogger, PHIGuard
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    """Fail closed if no API key is configured."""
    configured_key = os.getenv("AUDIT_API_KEY", "")
    if not configured_key:
        raise HTTPException(status_code=503, detail="Server API key not configured")
    if not x_api_key or not hmac.compare_digest(x_api_key, configured_key):
        raise HTTPException(status_code=401, detail="Invalid API key")


app = FastAPI(
    title="Sphincs Stateless Hash Sign API",
    description="Demonstration threshold-alert evaluator. Does not implement SLH-DSA signing or verification.",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "sphincs-stateless-hash-sign", "capability": "threshold-alert-demo", "slh_dsa_implemented": False, "version": "3.0.0"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "RUNNING"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload, _: None = Depends(require_api_key)):
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest, _: None = Depends(require_api_key)):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/audit/logs")
def api_audit_logs(_: None = Depends(require_api_key)):
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
