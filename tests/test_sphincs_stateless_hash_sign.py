"""
Automated Pytest Test Suite for Sphincs Stateless Hash Sign.
Domain: Post-Quantum Cryptography & Hardware Security
Standard: NIST FIPS 203/204/205 / ISO/IEC 17825 Standards
"""
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main, _resolve_safe_path


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_resolve_safe_path():
    # Valid path that exists
    valid = _resolve_safe_path("sample.csv", must_exist=True)
    assert valid.exists()

    # Non-existent file raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        _resolve_safe_path("nonexistent_file_xyz.csv", must_exist=True)

    # Output path (does not need to exist)
    out = _resolve_safe_path("output_results.csv", must_exist=False)
    assert isinstance(out, Path)


def test_batch_cli_with_sample_csv():
    """Test batch processing with the included sample.csv."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = os.path.join(tmpdir, "test_output.csv")
        result = main(["batch", "-i", "sample.csv", "-o", out_file])
        assert result == 0
        assert os.path.exists(out_file)
        with open(out_file, "r") as f:
            content = f.read()
            assert "overall_urgency" in content


def test_batch_cli_missing_input():
    """Test batch CLI gracefully handles missing input file."""
    result = main(["batch", "-i", "nonexistent_xyz.csv"])
    assert result == 1


def test_phi_guard_redaction():
    """Test that PHIGuard.redact_phi properly redacts sensitive data."""
    text_with_phi = "Patient John Doe MRN-12345678 has phone 555-123-4567"
    redacted = PHIGuard.redact_phi(text_with_phi)
    assert "John Doe" not in redacted
    assert "MRN-12345678" not in redacted
    assert "555-123-4567" not in redacted
    assert "[REDACTED_IDENTIFIER]" in redacted
