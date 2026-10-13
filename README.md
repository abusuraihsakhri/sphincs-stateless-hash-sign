# Sphincs Stateless Hash Sign

A deterministic **threshold-alert demonstration** with a Python CLI, FastAPI service, and standalone browser interface.

**Scope:** Despite the repository name, this project does **not** implement SPHINCS+, SLH-DSA, WOTS+, FORS, XMSS, cryptographic key generation, signature generation, or signature verification. Its arbitrary numeric thresholds and descriptor checks are **not** NIST FIPS 205 conformance criteria, nor is the project a FIPS-certified cryptographic implementation. See the [FIPS 205 standard](https://csrc.nist.gov/pubs/fips/205/final).

## Features

- Three deterministic workers evaluate a primary metric (example threshold 25), a secondary metric (example threshold 12), a critical flag, and anomaly keywords.
- Python CLI: single evaluation, batch CSV evaluation, chat/demo response, and in-process audit verification.
- HMAC-SHA256 chained **local audit log** with re-verification of message authentication codes; logs are process-local and ephemeral unless the application is extended with durable storage.
- FastAPI endpoints with API-key access control for evaluations, chat, and audit logs.
- An offline browser demo in [web/index.html](web/index.html). It runs entirely in JavaScript; no server, network calls, secrets, or browser Python runtime are required.

**Privacy:** The browser demo does not send entered values anywhere and does not store them. The API accepts user-provided values on the server and retains in-memory evaluation dossiers. The Python identifier filter uses limited regular expressions and is **not** a comprehensive PHI detector, de-identification process, or HIPAA compliance guarantee. Avoid using real patient identifiers.

## Python installation

Requires Python 3.9 or later (CI currently covers 3.10–3.12).

~~~bash
python -m pip install -e ".[dev]"
pytest -v
~~~

For CLI use without server/testing extras:

~~~bash
python -m pip install -e .
sphincs-stateless-hash-sign audit --task-id DEMO-001 --target KEY-01 --primary 29 --secondary 14
sphincs-stateless-hash-sign chat "What is this demo?"
sphincs-stateless-hash-sign batch -i sample.csv -o results.csv
sphincs-stateless-hash-sign verify-audit
~~~

An audit ledger exists only within a running Python process. Running `verify-audit` as a separate CLI process verifies its own ledger, **not** records from a prior command.

## Browser interface

Open `index.html` or `web/index.html` in a browser. The form evaluates the same example thresholds as the top-level Python workers and displays a locally calculated JSON dossier. No cryptographic signature or HMAC is produced by the browser. It is usable without Pyodide because the demonstration is straightforward JavaScript.

## REST API

~~~bash
export AUDIT_SECRET_KEY="replace-with-a-long-random-server-secret"
export AUDIT_API_KEY="replace-with-a-different-long-random-api-key"
python -m pip install -e ".[server]"
sphincs-stateless-hash-sign serve --host 127.0.0.1 --port 8000
curl -H "X-API-Key: $AUDIT_API_KEY" -H "Content-Type: application/json" \
  -d '{"task_id":"T-1","target_identifier":"EXAMPLE","primary_metric":29,"secondary_metric":14}' \
  http://127.0.0.1:8000/api/audit
~~~

`GET /health` and `GET /metrics` are public operational endpoints; `POST /api/audit`, `POST /api/chat`, and `GET /api/audit/logs` require `X-API-Key`. If no key is configured, protected endpoints fail closed. Do not expose the service directly to the public Internet without TLS, rate limiting, and additional security controls.

## Docker

Set `AUDIT_SECRET_KEY` and `AUDIT_API_KEY` in your shell or an untracked `.env` file (see `.env.example`), then run `docker compose up --build`. Docker Compose binds port 8000 to loopback only. Secrets must never be checked into Git.

## Development and limitations

Run `python -m compileall -q agents sphincs_hash_sign tests cli.py` and `pytest`; GitHub Actions executes this against multiple Python versions. The secondary `sphincs_hash_sign` package retains its earlier evaluation API, whereas the installed console script invokes the top-level CLI. The bundled test suite checks demonstration behavior, not FIPS 205 test vectors, side-channel resistance, or production security.

Technology: Python, Pydantic, FastAPI (optional), HTML, CSS, and JavaScript. The browser interface targets current evergreen desktop and mobile browsers. Licensed under the [MIT License](LICENSE).
