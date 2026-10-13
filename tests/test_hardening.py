"""Security and input-validation regression tests."""
import pytest
from pydantic import ValidationError
from agents.base import AuditTrail, PHIGuard, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from agents.llm_factory import LLMFactory


def test_hmac_chain_detects_entry_and_tag_tampering():
    ledger = AuditTrail(secret_key="unit-test-secret")
    first = ledger.log("user", "operator", "evaluate", {"outcome": "normal"})
    ledger.log("worker", "engine", "evaluate", {"outcome": "warning"})
    assert ledger.verify_integrity()
    ledger.logs[0]["event_type"] = "forged"
    assert not ledger.verify_integrity()
    ledger.logs[0]["event_type"] = "evaluate"
    assert ledger.verify_integrity()
    ledger.logs[1]["current_hash"] = "0" * 64
    assert not ledger.verify_integrity()


def test_ledger_snapshot_cannot_mutate_internal_state():
    ledger = AuditTrail(secret_key="unit-test-secret")
    ledger.log("worker", "engine", "evaluate", {"outcome": "normal"})
    snapshot = ledger.get_trail()
    snapshot[0]["actor"] = "forged"
    assert ledger.verify_integrity()
    assert ledger.get_trail()[0]["actor"] == "worker"


@pytest.mark.parametrize("invalid", [float("inf"), float("-inf"), float("nan")])
def test_metrics_must_be_finite(invalid):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="X", target_identifier="K", primary_metric=invalid)
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="X", target_identifier="K", primary_metric=1, secondary_metric=invalid)


def test_attributes_are_checked_for_sensitive_identifiers():
    payload = SystemTaskPayload(task_id="X", target_identifier="K",
                                primary_metric=1, attributes={"note": "MRN-12345678"})
    with pytest.raises(SecurityException):
        SystemSupervisor().process_task(payload)


def test_unsupported_llm_provider_not_silently_mocked():
    with pytest.raises(ValueError, match="Unsupported provider"):
        LLMFactory.create("openai")


def test_api_requires_key(monkeypatch):
    from fastapi.testclient import TestClient
    from agents.api import app
    client = TestClient(app)
    body = {"task_id": "T", "target_identifier": "K", "primary_metric": 3}
    monkeypatch.delenv("AUDIT_API_KEY", raising=False)
    assert client.post("/api/audit", json=body).status_code == 503
    monkeypatch.setenv("AUDIT_API_KEY", "local-test-api-key")
    assert client.post("/api/audit", json=body).status_code == 401
    assert client.get("/api/audit/logs").status_code == 401
    ok = client.post("/api/audit", json=body, headers={"X-API-Key": "local-test-api-key"})
    assert ok.status_code == 200
    assert ok.json()["overall_urgency"] == "ROUTINE"
    assert client.get("/api/audit/logs", headers={"X-API-Key": "local-test-api-key"}).status_code == 200
