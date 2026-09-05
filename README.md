# Sphincs Stateless Hash Sign

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Standards:** NIST FIPS 203/204/205, NIST SP 800-90B, ISO/IEC 17825

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Sphincs Stateless Hash Sign** is a post-quantum cryptographic analytical platform implementing NIST FIPS 205 SLH-DSA stateless hash-based signature supervision with WOTS+ and FORS trees. It provides multi-worker evaluation, HMAC-SHA256 tamper-evident audit trails, and zero-PHI outbound data protection.

---

## ⚙️ Key Capabilities

- **Multi-Worker Evaluation:** InvariantQCWorker, SafetyEscalationWorker, and ProtocolConformanceWorker analyze payloads with domain-specific thresholds.
- **HMAC-SHA256 Audit Trail:** Cryptographically chained, tamper-evident logs for every task evaluation and state transition.
- **Zero-PHI Outbound Guard:** Active pattern inspection blocking SSNs, MRNs, phone numbers, and patient identifiers from outbound data.
- **FastAPI REST API:** OpenAPI 3.1 endpoints with health, metrics, audit, and chat capabilities.
- **Prometheus Telemetry:** Operational metrics export at `/metrics`.
- **Batch Processing:** CSV batch input/output for high-throughput evaluation.
- **Active Learning Calibration:** Bayesian weight tracking for worker reliability.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/sphincs-stateless-hash-sign.git
cd sphincs-stateless-hash-sign

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Optional: Set audit secret key (recommended for production)
export AUDIT_SECRET_KEY="your-secure-random-key-here"
```

---

## 💻 CLI Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Supervisory Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### CLI Parameters

| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task identifier | TASK-2026-001 |
| `--target` | Target entity identifier | KEY-TARGET-01 |
| `--primary` | Primary metric value (float) | 28.5 |
| `--secondary` | Secondary metric value (float) | 14.2 |
| `--critical` | Enable critical flag | False |
| `--status` | Status descriptor | DISCORDANT |
| `-i, --input` | Batch input CSV path (required for batch) | - |
| `-o, --output` | Batch output CSV path | results.csv |

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| GET | `/health` | System health check |
| GET | `/metrics` | Prometheus operational metrics |
| POST | `/api/audit` | Submit task for evaluation |
| POST | `/api/chat` | Supervisory chat query |
| GET | `/api/audit/logs` | Retrieve and verify HMAC audit trail |

---

## 🧪 Testing

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
docker build -t sphincs-stateless-hash-sign .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key sphincs-stateless-hash-sign
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 🛡️ Security Architecture

- **Zero-PHI Outbound Interceptor:** AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
- **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation.
- **Input Validation:** Path traversal protection and bounds checking on all CLI inputs.
- **Ephemeral Key Generation:** If `AUDIT_SECRET_KEY` is not set, a random session key is generated with a warning.

---

## 📁 Project Structure

```
sphincs-stateless-hash-sign/
├── agents/                  # Enterprise multi-worker evaluation engine
│   ├── api.py              # FastAPI REST server
│   ├── base.py             # Security, PHI guard, HMAC audit trail
│   ├── models.py           # Pydantic data models
│   ├── supervisor.py       # Master orchestrator
│   ├── workers.py          # Specialized evaluation workers
│   ├── metrics.py          # Prometheus metrics collector
│   ├── streamer.py         # WebSocket telemetry broadcaster
│   ├── learning.py         # Bayesian calibration engine
│   └── llm_factory.py      # LLM provider factory
├── sphincs_hash_sign/      # Frontier SLH-DSA implementation
│   ├── cli.py              # Frontier CLI
│   ├── server.py           # Frontier FastAPI server
│   ├── engine.py           # Core algorithmic engine
│   ├── agents.py           # WOTS+, FORS, Hypertree agents
│   └── models.py           # Frontier data models
├── tests/                  # Pytest test suite
├── web/index.html          # Operations console UI
├── cli.py                  # Main CLI entry point
├── simulator.py            # High-throughput simulation
├── enrichment.py           # Domain enrichment features
├── pyproject.toml          # Project configuration
├── Dockerfile              # Container build
└── docker-compose.yml      # Container orchestration
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
