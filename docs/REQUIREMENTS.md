# REQUIREMENTS.md  

## 1. Overview  
The **medic‑verify** project provides a lightweight, programmatic marketplace for certified machine‑learning models. It enables developers to register models, query the catalog, and retrieve a compliance package that contains all artefacts required for regulatory or internal audit (e.g., model metadata, version hash, provenance, and certification documents).  

The library is intended for use as a Python package that can be embedded in CI pipelines, model‑registry services, or edge‑deployment tools.  

---

## 2. Functional Requirements  

| ID | Description |
|----|-------------|
| **FR‑1** | **Marketplace Instantiation** – The library shall expose a `Marketplace` class that can be instantiated with optional configuration parameters: `storage_backend`, `compliance_schema`, and `audit_logger`. |
| **FR‑2** | **Add Model** – `Marketplace.add_model(model_id: str, version: str, metadata: dict, compliance_package: bytes) → None` shall register a new model. The method must validate that `model_id` + `version` is unique; otherwise raise `DuplicateModelError`. |
| **FR‑3** | **Update Model** – `Marketplace.update_model(model_id: str, version: str, metadata: dict = None, compliance_package: bytes = None) → None` shall allow partial updates of metadata or compliance artefacts for an existing entry. |
| **FR‑4** | **List Models** – `Marketplace.list_models(filter: dict = None) → List[ModelInfo]` shall return a list of model descriptors (`model_id`, `version`, `created_at`, `status`). Filtering may be performed on any metadata field. |
| **FR‑5** | **Get Compliance Package** – `Marketplace.get_compliance_package(model_id: str, version: str) → bytes` shall retrieve the stored compliance package for the specified model version. If not found, raise `ModelNotFoundError`. |
| **FR‑6** | **Delete Model** – `Marketplace.delete_model(model_id: str, version: str) → None` shall permanently remove a model entry and its compliance artefacts. |
| **FR‑7** | **Search by Certification** – `Marketplace.search_by_cert(cert_type: str) → List[ModelInfo]` shall return all models that contain a compliance package with the given certification type (e.g., “FDA‑21‑CFR‑Part‑11”). |
| **FR‑8** | **Audit Logging** – Every mutating operation (`add`, `update`, `delete`) shall emit a structured log entry to the configured `audit_logger` with timestamp, operation, user‑context (if supplied), and outcome. |
| **FR‑9** | **Persistence Backend** – The default storage backend shall be an on‑disk SQLite database (`medic_verify.db`). The design shall allow plugging alternative backends (e.g., PostgreSQL, Redis) via the `storage_backend` interface. |
| **FR‑10** | **Schema Validation** – Compliance packages must conform to a JSON‑Schema supplied at `Marketplace` construction (`compliance_schema`). Validation errors must be reported as `ComplianceSchemaError`. |
| **FR‑11** | **Thread‑Safety** – All public methods shall be safe to call from multiple threads/processes when using the default SQLite backend (i.e., use appropriate transaction isolation). |
| **FR‑12** | **Versioning Semantics** – Versions follow [Semantic Versioning 2.0.0](https://semver.org). The system shall reject non‑semantic version strings with `InvalidVersionError`. |
| **FR‑13** | **Export / Import** – Provide `export_catalog(path: str) → None` and `import_catalog(path: str) → None` to dump/load the entire marketplace (metadata + compliance packages) as a single ZIP archive. |
| **FR‑14** | **CLI Wrapper** – A minimal command‑line interface (`medic-verify-cli`) shall expose the above operations for scripting and manual use. |
| **FR‑15** | **Documentation Generation** – The package shall include auto‑generated API docs (via Sphinx) and a README with usage examples. |

---

## 3. Non‑Functional Requirements  

| ID | Requirement |
|----|-------------|
| **NFR‑1** | **Performance** – `list_models` and `search_by_cert` shall return results for catalogs up to 100 k entries in ≤ 200 ms (average) on commodity hardware (Intel i5, 8 GB RAM). |
| **NFR‑2** | **Scalability** – The storage‑backend interface shall support horizontal scaling; when swapped to a distributed DB (e.g., PostgreSQL), the same API must handle ≥ 1 M models without code changes. |
| **NFR‑3** | **Security – Data at Rest** – Compliance packages (binary blobs) must be stored encrypted using AES‑256‑GCM. The encryption key is supplied via environment variable `MEDIC_VERIFY_KEY` or a KMS integration. |
| **NFR‑4** | **Security – Access Control** – The library shall accept an optional `auth_provider` callable that validates the current user context; all mutating operations must invoke it and raise `UnauthorizedError` on failure. |
| **NFR‑5** | **Reliability** – All write operations shall be atomic; in case of failure, the database must roll back to the previous consistent state. |
| **NFR‑6** | **Durability** – Once a transaction commits, the data must survive process crashes and power loss (SQLite `PRAGMA journal_mode=WAL`). |
| **NFR‑7** | **Observability** – Emit Prometheus‑compatible metrics: `medic_verify_models_total`, `medic_verify_additions_total`, `medic_verify_errors_total` (labelled by error type). |
| **NFR‑8** | **Portability** – The package shall be pure Python 3.10+ with no compiled extensions, enabling installation on Linux, macOS, and Windows via `pip`. |
| **NFR‑9** | **Testing** – Achieve ≥ 90 % unit‑test coverage, including property‑based tests for version parsing and schema validation. |
| **NFR‑10** | **Compliance** – The library must be released under the Apache‑2.0 license and include a SPDX identifier in every source file. |
| **NFR‑11** | **Documentation** – API reference, quick‑start guide, and architecture diagram must be hosted on the project’s GitHub Pages and kept in sync with code. |
| **NFR‑12** | **Maintainability** – Code shall follow the company’s style guide (PEP 8 + mypy strict typing). All public classes/functions must have docstrings with type hints. |

---

## 4. Constraints  

1. **Dependency Policy** – Only third‑party packages with permissive licenses (Apache‑2.0, MIT, BSD) may be added. Core dependencies are limited to: `sqlite3` (stdlib), `pydantic` (schema validation), `cryptography` (AES‑GCM), `prometheus-client`, and `click` (CLI).  
2. **Runtime Environment** – Must run on the standard Axentx OS container image (Ubuntu 22.04, Python 3.10). No OS‑level services (e.g., external DB) are assumed for the default deployment.  
3. **Data Size** – Individual compliance packages shall not exceed 50 MiB; larger artefacts must be stored externally and referenced via URI in metadata.  
4. **Backward Compatibility** – Future releases must preserve the public API contract; deprecations must follow a 2‑release cycle with warnings.  

---

## 5. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Users of the library will manage their own authentication context and supply a callable to `Marketplace` when needed. |
| **A‑2** | The encryption key (`MEDIC_VERIFY_KEY`) will be provisioned securely in the deployment environment; key rotation is out of scope for the initial release. |
| **A‑3** | Model owners will provide compliance packages that already contain any required regulatory signatures; the system only validates schema conformity. |
| **A‑4** | The marketplace will be used primarily in internal pipelines; public multi‑tenant SaaS exposure is not a target for v1.0. |
| **A‑5** | The JSON‑Schema for compliance packages will be supplied by the product team and will not change more than once per major release. |
| **A‑6** | The default SQLite file will reside on a volume that is backed up by the organization’s standard backup process. |
| **A‑7** | The CLI will be executed by technical users; interactive prompts are not required. |

---

## 6. Acceptance Criteria  

- All functional requirements (FR‑1 – FR‑15) are implemented and pass integration tests.  
- Non‑functional thresholds (NFR‑1 – NFR‑12) are verified via benchmark and security test suites.  
- Documentation builds without errors and the CLI displays help text for every command.  
- The package can be installed via `pip install .` from a clean virtual environment and all unit tests pass (`pytest -q`).  

---  

*Prepared by the senior product/engineering lead, 2026‑06‑24.*
