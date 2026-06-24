# STORIES.md  

## Project: **medic-verify**  
*Simple marketplace for certified AI models – a registry that stores model metadata, tracks compliance certifications, and generates compliance packages for downstream consumers.*

---

## Epics & Backlog  

| Epic | Description | MVP Priority |
|------|-------------|--------------|
| **E1 – Core Marketplace API** | Provide a clean, type‑safe API to create a marketplace, add models, list them, and retrieve compliance packages. | ✅ |
| **E2 – Model Certification Management** | Enable model owners to upload certification artifacts (e.g., audit reports, test results) and associate them with a model version. | ⬜ |
| **E3 – Access Control & Auditing** | Restrict who can add or modify models and keep an immutable audit log of all actions. | ⬜ |
| **E4 – Search & Filtering** | Allow consumers to search models by tags, domain, compliance level, and version. | ⬜ |
| **E5 – Export & Integration** | Produce a signed compliance package (JSON + signature) that can be consumed by external pipelines. | ⬜ |
| **E6 – UI Dashboard (optional stretch)** | Minimal web UI to view the catalog and download compliance packages. | ⬜ |

> **MVP** = all stories in **E1** plus the minimal subset of **E2** needed to generate a compliance package.

---

## User Stories  

### **Epic E1 – Core Marketplace API**

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E1‑01** | **As a developer, I want to instantiate a `Marketplace` object, so that I can start using the catalog in my application.** | - `Marketplace()` can be called with optional configuration (e.g., storage backend).<br>- The instance exposes `add_model`, `list_models`, `get_compliance_package` methods.<br>- No exceptions are raised on construction. |
| **E1‑02** | **As a model owner, I want to add a new model with its metadata, so that it becomes discoverable in the marketplace.** | - `add_model(model_id: str, version: str, metadata: dict)` returns a success flag or raises a clear error.<br>- Duplicate `model_id + version` pairs are rejected with a specific `ModelExistsError`.<br>- Stored metadata includes at least `name`, `description`, `tags`, `owner`, `created_at`. |
| **E1‑03** | **As a consumer, I want to list all models, so that I can browse the catalog.** | - `list_models()` returns a list of model summary objects (id, version, name, tags).<br>- The list is ordered by `created_at` descending by default.<br>- Supports optional pagination parameters (`limit`, `offset`). |
| **E1‑04** | **As a compliance officer, I want to retrieve a compliance package for a specific model version, so that I can ship it to downstream users.** | - `get_compliance_package(model_id: str, version: str)` returns a `CompliancePackage` object containing:<br> • Model metadata<br> • List of attached certification artifacts (file names, hashes)<br> • Generation timestamp<br>- If the model/version does not exist, a `ModelNotFoundError` is raised.<br>- The package can be serialized to JSON via `to_json()`. |
| **E1‑05** | **As a developer, I want the marketplace to persist data across process restarts, so that the catalog is durable.** | - By default, data is stored in an on‑disk SQLite file (`medic_verify.db`).<br>- After process termination and restart, previously added models are still returned by `list_models()`. |
| **E1‑06** | **As a tester, I want comprehensive unit tests for the core API, so that regressions are caught early.** | - Test suite covers happy paths and error cases for all E1 methods.<br>- CI pipeline runs `pytest` and fails on any test regression. |

### **Epic E2 – Model Certification Management**

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E2‑01** | **As a model owner, I want to upload certification artifacts (PDF, CSV, etc.) when adding a model, so that the marketplace records evidence of compliance.** | - `add_model` accepts an optional `cert_files: List[Path]` argument.<br>- Files are copied into a protected `certificates/` directory with a deterministic naming scheme (`{model_id}_{version}_{hash}.{ext}`).<br>- File SHA‑256 hashes are stored in the model record. |
| **E2‑02** | **As a compliance reviewer, I want to view the list of attached certificates for a model version, so that I can verify completeness.** | - `get_compliance_package` includes a `certificates` array with `{filename, sha256, uploaded_at}` entries.<br>- Missing certificates are reported with a warning flag in the package. |
| **E2‑03** | **As a security auditor, I want certificates to be immutable after upload, so that tampering is detectable.** | - Uploaded files are write‑once; subsequent `add_model` calls with the same `model_id`/`version` cannot replace existing certificates.<br>- Attempting to replace returns `CertificateImmutableError`. |
| **E2‑04** | **As a downstream consumer, I want the compliance package to be signed, so that I can verify its integrity.** | - `CompliancePackage.sign(private_key: RSAKey)` produces a Base64‑encoded signature attached to the JSON payload.<br>- `CompliancePackage.verify(public_key: RSAKey)` returns `True` for a valid signature and raises `SignatureVerificationError` otherwise. |
| **E2‑05** | **As a product manager, I want a CLI command `medic-verify export <model_id> <version>` that writes the signed compliance package to a file, so that non‑programmatic users can obtain it.** | - CLI prints a helpful usage message.<br>- On success, creates `<model_id>_<version>_compliance.json` in the current directory.<br>- Returns non‑zero exit code on any error, with a clear message. |

### **Epic E3 – Access Control & Auditing** *(stretch)*

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E3‑01** | **As an admin, I want role‑based permissions (owner, reviewer, consumer), so that only authorized users can add or modify models.** | - `Marketplace` accepts a `UserContext` (user_id, role).<br>- `add_model` checks that `role` is `owner` or `admin`.<br>- Unauthorized attempts raise `PermissionDeniedError`. |
| **E3‑02** | **As an auditor, I want an immutable audit log of all actions, so that we have traceability.** | - Every API call that mutates state writes a JSON line to `audit.log` with timestamp, user_id, action, model_id, version, outcome.<br>- Log file is append‑only and tamper‑evident (hash chain). |

### **Epic E4 – Search & Filtering** *(stretch)*

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E4‑01** | **As a consumer, I want to filter models by tag and compliance level, so that I can quickly find suitable models.** | - `list_models(filter: dict)` supports keys `tags`, `owner`, `has_certificates`.<br>- Returns only models matching **all** supplied criteria. |
| **E4‑02** | **As a developer, I want full‑text search on model name/description, so that users can search by keywords.** | - Integrated with SQLite FTS5; `list_models(search="keyword")` returns relevant matches ordered by relevance score. |

### **Epic E5 – Export & Integration** *(stretch)*

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E5‑01** | **As a CI pipeline, I want to fetch a compliance package via HTTP, so that builds can automatically verify model provenance.** | - Simple Flask (or FastAPI) server exposing `/models/<id>/<ver>/compliance` returning signed JSON.<br>- Endpoint respects `If-None-Match` ETag for caching. |
| **E5‑02** | **As a downstream service, I want to validate the package signature using a public key bundle, so that I can trust the data without contacting Axentx.** | - Documentation includes example verification script in Python and Bash.<br>- Public key is distributed via a well‑known URL (`/public_key.pem`). |

### **Epic E6 – UI Dashboard** *(optional stretch)*

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E6‑01** | **As a product owner, I want a minimal web UI to browse models and download compliance packages, so that non‑technical stakeholders can use the marketplace.** | - React (or plain HTML) page listing models with “Download Package” button.<br>- UI consumes the same REST endpoints as the server.<br>- Deployed via `npm run start` in a Docker container. |

---

## Prioritization for MVP (Release 1.0)

1. **E1‑01 → E1‑06** – Core API, persistence, and test coverage.  
2. **E2‑01 → E2‑04** – Certificate upload, immutable storage, signed package generation.  
3. **E2‑05** – CLI export (adds immediate value for non‑dev users).  

All other epics are slated for subsequent releases after validation of market interest.

---  

*Prepared by the Product/Engineering Lead – Axentx OS*  
*Date: 2026‑06‑24*
