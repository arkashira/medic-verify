# ROADMAP.md – medic‑verify

## Vision
Create a lightweight, standards‑compliant marketplace that lets AI model developers publish **certified** models and enables downstream users to retrieve a **compliance package** (metadata, provenance, test reports, licensing) in a single API call. The platform will be the go‑to “app store” for trustworthy models, reducing friction for regulated industries (healthcare, finance, autonomous systems).

---

## MVP – **Launch‑Ready Core** *(Critical)*

| Milestone | Description | Acceptance Criteria |
|-----------|-------------|---------------------|
| **M1: Marketplace Core API** | Implement `Marketplace` class with in‑memory store. | - `add_model(model_id, metadata)` persists model.<br>- `list_models()` returns all model IDs.<br>- `get_compliance_package(model_id)` returns a JSON package containing:<br> • Model ID<br> • Version<br> • Certification authority<br> • Test results summary<br> • License info |
| **M2: Model Certification Schema** | Define JSON schema for a **Compliance Package** (v1). | - Schema validated on `add_model`.<br>- Includes required fields: `model_id`, `version`, `certifier`, `test_report_url`, `license`. |
| **M3: Persistence Layer** | Swap in‑memory store for a lightweight SQLite backend. | - Data survives process restart.<br>- Simple migration script included. |
| **M4: CLI & Basic Docs** | Provide a command‑line tool (`medic-verify-cli`) and README usage examples. | - `medic-verify add`, `list`, `get` commands work.<br>- Auto‑generated API docs via `mkdocstrings`. |
| **M5: CI/CD & Test Coverage** | GitHub Actions pipeline with unit tests (≥80% coverage). | - Tests for all public methods.<br>- Linting (ruff/black) and type‑checking (mypy). |
| **M6: Security Baseline** | Input validation, rate‑limiting stub, and secret handling. | - No arbitrary code execution via metadata.<br>- Secrets (e.g., API keys for external certifiers) stored in `.env`. |

**MVP Success Metric:** Deployable Docker image that passes all CI checks and can be spun up locally with a single `docker compose up`.  

---

## Phase 1 – **Enterprise‑Ready Extensions** (v1)

| Theme | Feature | Target Release |
|-------|---------|-----------------|
| **Authentication & Authorization** | OAuth2 / API‑key support; role‑based access (publisher vs consumer). | Q3 2026 |
| **External Certification Integration** | Plug‑in adapters for popular certifiers (e.g., ISO‑9001, FDA‑AI, EU AI Act). | Q3 2026 |
| **Versioning & Roll‑back** | Full model version lifecycle, immutable compliance packages, rollback to prior certified version. | Q4 2026 |
| **Web UI Dashboard** | Minimal React front‑end: model catalog, compliance details, upload wizard. | Q4 2026 |
| **Audit Logging** | Append‑only log of all marketplace actions (JSON‑Lines, optional ELK export). | Q4 2026 |
| **Metrics & Billing Hooks** | Export usage metrics (API calls, model downloads) and optional Stripe integration for paid listings. | Q4 2026 |

**Key KPI:** 10+ paying enterprise customers onboarded; ≥95% API success rate.

---

## Phase 2 – **Ecosystem & Scale** (v2)

| Theme | Feature | Target Release |
|-------|---------|-----------------|
| **Federated Marketplace** | Peer‑to‑peer sync of compliant models across multiple `medic-verify` instances (multi‑tenant). | Q2 2027 |
| **Policy Engine** | Declarative policy language (OPA‑style) to enforce custom compliance rules per consumer. | Q2 2027 |
| **AI‑Assisted Certification** | Integration with vLLM inference to auto‑generate preliminary test reports for new models. | Q3 2027 |
| **Marketplace SDKs** | First‑class client libraries for Python, Go, and JavaScript. | Q3 2027 |
| **Compliance Package Standards** | Support for emerging standards (e.g., IEEE 7000, ISO/IEC 42001). | Q4 2027 |
| **High‑Availability Deployment** | Kubernetes operator, PostgreSQL HA, horizontal scaling of API pods. | Q4 2027 |

**Long‑term Goal:** Become the de‑facto compliance hub for regulated AI, handling >100k certified models with sub‑second latency.

---

## Milestone Timeline (High‑Level)

| Quarter | Deliverable |
|---------|-------------|
| **Q2 2026** | MVP (Core API, SQLite, CLI, CI) – Release candidate |
| **Q3 2026** | Auth, external certifier adapters, versioning |
| **Q4 2026** | Web UI, audit logs, metrics/billing |
| **Q1 2027** | Customer pilots, feedback loop, iterate on UX |
| **Q2 2027** | Federated sync, policy engine |
| **Q3 2027** | AI‑assisted certification, SDKs |
| **Q4 2027** | HA Kubernetes deployment, standards extensions |

---

## Success Metrics & Validation

| Metric | Target |
|--------|--------|
| **Time‑to‑certify** (model upload → compliance package) | ≤ 5 min (post‑v1) |
| **API Latency** (99th percentile) | ≤ 200 ms |
| **Customer Retention (MRR)** | ≥ 90% after 6 months |
| **Compliance Accuracy** | 0 false‑positive/negative certifications in audit (verified by external auditors) |
| **Revenue** | $150k ARR by end of 2027 |

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Regulatory change** | May invalidate schema | Design schema as extensible; maintain a versioned spec repo. |
| **Data privacy** (model metadata leakage) | Legal/brand risk | Encrypt stored metadata at rest; strict access controls. |
| **Adoption barrier** (trust in certifiers) | Low market traction | Partner early with recognized certifiers; provide transparent audit trails. |
| **Scalability** (single SQLite) | Performance bottleneck | Planned migration to PostgreSQL in v2 HA rollout. |

---

*Prepared by the Product & Engineering Lead, medic‑verify – June 2026*
