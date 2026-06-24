# Medic‑Verify PRD  

**Document Version:** 1.0  
**Date:** 2026‑06‑24  
**Author:** Senior Product/Engineering Lead, Axentx OS  

---  

## 1. Problem Statement  

Healthcare AI/ML models are increasingly deployed in clinical workflows, but regulators, hospitals, and insurers demand **formal proof of compliance** (e.g., FDA/EMA clearance, data‑privacy attestations, bias audits).  
Currently:

* Vendors ship models without a standardized, machine‑readable compliance package.  
* Buyers spend weeks manually gathering certificates, test reports, and usage constraints.  
* Lack of a **trusted marketplace** leads to duplicated due diligence, delayed adoption, and higher legal risk.  

**Medic‑Verify** solves this by providing a lightweight, programmable marketplace where model creators can attach verified compliance artifacts, and downstream users can retrieve a complete, signed compliance package with a single API call.

---  

## 2. Target Users  

| Persona | Primary Need | How Medic‑Verify Helps |
|---------|--------------|------------------------|
| **AI Model Vendors** (start‑ups, med‑tech firms) | Demonstrate regulatory clearance quickly; differentiate with “certified” badge. | Publish models with attached compliance artifacts (regulatory filings, bias audit reports, data‑source provenance). |
| **Hospital Procurement Teams** | Reduce time spent on compliance review; ensure legal safety. | Query marketplace, receive a signed compliance package ready for internal audit. |
| **Regulators / Auditors** | Verify that a model’s claimed certifications are authentic and immutable. | Access cryptographically‑signed compliance bundles; validate signatures against a public key registry. |
| **Integrators / MLOps Engineers** | Automate model ingestion pipelines with compliance gating. | Pull compliance package via SDK, enforce policy checks before deployment. |

---  

## 3. Goals & Success Metrics  

| Goal | Success Metric | Target |
|------|----------------|--------|
| **Accelerate compliance onboarding** | Avg. time from model discovery to compliance package receipt | ≤ 5 minutes |
| **Increase marketplace adoption** | Number of active certified models | ≥ 150 models within 6 months |
| **Reduce manual due‑diligence effort** | Avg. hours spent per model review by procurement | ≤ 0.5 h |
| **Maintain trustworthiness** | % of compliance packages that pass cryptographic verification | 100 % |
| **Revenue generation** | Paid “Verified” badge subscriptions (monthly) | $12 k ARR by month 4 |

---  

## 4. Scope  

### In‑Scope (MVP)

1. **Marketplace Core API**  
   * `Marketplace` class (Python) with methods:  
     - `add_model(model_id: str, metadata: dict, compliance_artifacts: dict) -> None`  
     - `list_models(filter: dict = None) -> List[ModelInfo]`  
     - `get_compliance_package(model_id: str) -> CompliancePackage`  

2. **Compliance Package Format**  
   * JSON‑LD container bundling:  
     - Regulatory certificates (PDF/JSON)  
     - Bias audit reports (CSV/JSON)  
     - Data‑source provenance (hashes, lineage)  
     - Signed manifest (RSA‑2048, SHA‑256)  

3. **Signature & Verification**  
   * Private signing key per vendor (stored in a secure vault).  
   * Public key registry endpoint (`/registry`) for auditors to fetch keys.  

4. **CLI / SDK**  
   * Simple Python CLI (`medic-verify-cli`) for adding models and retrieving packages.  
   * SDK wrapper for programmatic access (installable via pip).  

5. **Documentation & Samples**  
   * README with usage walkthrough.  
   * Example notebooks demonstrating end‑to‑end compliance retrieval.  

6. **Testing & CI**  
   * Unit tests covering all public methods (≥ 90 % coverage).  
   * GitHub Actions pipeline for linting, testing, and publishing the package to PyPI (internal test index).  

### Out‑of‑Scope (Future Phases)

| Feature | Reason |
|---------|--------|
| **Web UI marketplace portal** | MVP focuses on API/SDK; UI will be built after market traction. |
| **Automated compliance validation (e.g., AI‑driven bias detection)** | Requires separate ML pipeline; out of scope for the compliance‑packaging layer. |
| **Multi‑cloud storage back‑ends** | Initial implementation uses local file system / S3‑compatible bucket; abstraction added later. |
| **Marketplace monetisation beyond badge subscriptions** | Additional pricing models (transaction fees, enterprise licensing) planned for Phase 2. |
| **Support for non‑Python runtimes** | Current target audience is Python‑centric; wrappers for Java/Go can be added later. |

---  

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **Model Registration (`add_model`)** | Vendors upload model ID, metadata, and a set of compliance artifacts. | - Returns `201 Created` on success.<br>- Rejects if required artifacts missing.<br>- Stores artifacts immutably (append‑only). |
| **P1** | **Compliance Package Retrieval (`get_compliance_package`)** | Consumers receive a signed bundle ready for audit. | - Returns a `CompliancePackage` object containing all artifacts and a valid signature.<br>- Signature verification succeeds against vendor’s public key. |
| **P1** | **Artifact Signing** | Automatic creation of a manifest and RSA signature. | - Manifest includes SHA‑256 digests of each artifact.<br>- Signature is verifiable with the public key registry. |
| **P2** | **Public Key Registry Service** | HTTP endpoint exposing vendor public keys. | - `GET /registry/{vendor_id}` returns PEM‑encoded key.<br>- Keys rotate securely with revocation support. |
| **P2** | **CLI Tool** | `medic-verify-cli` for quick add/list/get operations. | - `medic-verify-cli add …` uploads artifacts and prints confirmation.<br>- `medic-verify-cli get …` writes package to a user‑specified directory. |
| **P3** | **Search / Filtering** | `list_models` supports filters (e.g., specialty, clearance level). | - Returns paginated results matching filter criteria.<br>- Supports sorting by `last_updated`. |
| **P3** | **Audit Log** | Immutable log of all add/list/get actions per model. | - Log entries stored in append‑only storage.<br>- Accessible via `GET /audit/{model_id}` (read‑only). |
| **P4** | **Integration Hooks** | Webhook callbacks on new model registration for downstream pipelines. | - Configurable URL per vendor.<br>- Payload includes model ID and compliance hash. |

---  

## 6. Success Metrics Implementation  

| Metric | Data Source | Collection Method |
|--------|-------------|-------------------|
| Avg. time to retrieve compliance package | API latency logs | Prometheus histogram on `/get_compliance_package` |
| Active certified models count | Marketplace DB (`models` table) | Daily aggregation job |
| Procurement hours saved | Survey of pilot customers (quarterly) | Qualitative KPI, mapped to quantitative estimate |
| Verification pass rate | Signature verification logs | Counter of `verify_success` vs `verify_failure` |
| ARR from badge subscriptions | Billing system (Stripe) | Monthly revenue report |

---  

## 7. Risks & Mitigations  

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Key compromise** – private signing key leaked. | Loss of trust, legal exposure. | Store keys in HSM‑backed vault (AWS KMS / HashiCorp Vault). Enforce rotation policy every 90 days. |
| **Artifact tampering** – stored files altered after signing. | Invalid compliance evidence. | Use immutable storage (S3 Object Lock or append‑only DB). Include artifact digests in manifest. |
| **Regulatory variance** – differing certificate formats across regions. | Integration friction. | Define a flexible schema (JSON‑LD) that can embed any document type; provide adapters in SDK. |
| **Adoption hurdle** – vendors reluctant to expose certificates. | Low marketplace content. | Offer “Verified Badge” subscription that adds marketing exposure and analytics dashboard. |
| **Performance at scale** – large artifact files (e.g., 500 MB PDFs). | Slow uploads/downloads. | Support multipart upload to S3; enable CDN caching for retrieval. |

---  

## 8. Timeline (MVP – 12 weeks)

| Week | Milestone |
|------|-----------|
| 1‑2 | Project kickoff, detailed design, repository scaffolding. |
| 3‑4 | Implement `Marketplace` core class, data model, and storage layer. |
| 5‑6 | Add artifact signing, public key registry service, and verification utilities. |
| 7‑8 | Build CLI tool, SDK wrapper, and documentation. |
| 9 | Write unit/integration tests, set up CI pipeline. |
| 10 | Internal security review (key handling, immutability). |
| 11 | Pilot with 2 vendor partners (feedback loop). |
| 12 | Release MVP to internal beta, prepare marketing “Verified Badge” page. |

---  

## 9. Open Questions  

1. **Compliance Artifact Standards** – Should we enforce a specific schema (e.g., HL7 FHIR) or remain schema‑agnostic?  
2. **Pricing Model** – What tiered pricing should the “Verified Badge” have (per‑model vs per‑vendor)?  
3. **Governance** – Will Axentx act as a certifier or only a conduit? Need legal review.  

---  

*Prepared for the Axentx product development pipeline. This PRD is intended to be a concrete, shippable specification for the first release of Medic‑Verify.*
