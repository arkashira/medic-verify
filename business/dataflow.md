# dataflow.md  

## System Dataflow Architecture  

```
+-------------------+        +-------------------+        +-------------------+
| External Data     |  -->   | Ingestion Layer   |  -->   | Processing /      |
| Sources           |        | (API Gateway,     |        | Transform Layer   |
|-------------------|        |  Auth Service)    |        | (Validator,       |
| • EMR / EHR APIs   |        |-------------------|        |  Sanitizer,       |
| • Imaging PACS     |        | • API Gateway     |        |  Bias‑Mitigator) |
| • Lab Result Feeds|        | • OAuth2 / OIDC   |        |-------------------|
| • Device Telemetry|        |   Auth Service    |        | • Data Validation |
| • Public Health   |        | • Rate Limiter    |        |   Engine (accuracy|
|   Datasets (FHIR) |        | • Input Queue (Kafka)      |   drift, etc.)   |
+-------------------+        +-------------------+        | • PII Scrubber   |
                                                          | • Model‑Specific |
                                                          |   Consistency    |
                                                          +-------------------+
        |                                 |                     |
        v                                 v                     v
+-------------------+        +-------------------+        +-------------------+
| Storage Tier      |  <--   | Query / Serving   |  <--   | Egress to User    |
|-------------------|        | Layer             |        | (Dashboard, API) |
| • Raw Data Lake   |        |-------------------|        |-------------------|
|   (S3 / GCS)      |        | • Search Service |        | • Authenticated   |
| • Processed DB    |        |   (ElasticSearch) |        |   UI (React)      |
|   (PostgreSQL)    |        | • GraphQL API     |        | • Export API (REST)|
| • Model Metrics   |        |   (Apollo)        |        |   (OAuth2)        |
|   Store (TimescaleDB)        | • Cache (Redis)   |        | • Alerting (Webhook)|
+-------------------+        +-------------------+        +-------------------+
```

---

### 1. External Data Sources  
- **EMR/EHR APIs** (FHIR‑based, HL7) – patient demographics, diagnoses, medication orders.  
- **Imaging PACS** (DICOM) – radiology images, reports.  
- **Lab Result Feeds** (HL7 v2, JSON) – pathology, blood work.  
- **Device Telemetry** (IoT, MQTT) – vitals monitors, wearables.  
- **Public Health Datasets** (CDC, WHO) – disease prevalence, benchmarks.  

All external sources must present **OAuth2 / OIDC** tokens issued by the **Ingestion Auth Service**; otherwise traffic is rejected at the API Gateway.

---

### 2. Ingestion Layer  
| Component | Role | Auth / Security |
|-----------|------|-----------------|
| **API Gateway** | Unified entry point; request routing, TLS termination. | Mutual TLS + OAuth2 scopes (`ingest:read`). |
| **Auth Service** | Issues and validates JWTs; integrates with corporate IdP (Okta). | Centralized policy enforcement (OPA). |
| **Rate Limiter** | Prevents abuse, protects downstream services. | Enforced per‑client quota. |
| **Input Queue** (Kafka) | Buffering, decoupling ingestion from processing. | ACLs on topics (`raw-ingest`). |
| **Connector Workers** | Pull data from source APIs (FHIR client, DICOM listener). | Service‑to‑service credentials (client‑cert). |

---

### 3. Processing / Transform Layer  
| Component | Function | Auth / Security |
|-----------|----------|-----------------|
| **Validator Engine** | Checks schema compliance, model‑specific performance contracts (e.g., AUROC ≥ 0.85). | Runs inside a sandbox; only internal service accounts. |
| **PII Scrubber** | Redacts PHI per HIPAA (de‑identification). | Access limited to `processor:scrub` role. |
| **Bias‑Mitigator** | Detects demographic skew, applies re‑weighting. | Auditable logs, signed by processing key. |
| **Consistency Enforcer** | Ensures same input yields same output across model versions. | Immutable configuration stored in Config Service. |
| **Transform Workers** (Spark/Flink) | Batch / stream transformations, feature extraction. | Kerberos‑authenticated; data‑at‑rest encryption. |
| **Metrics Collector** | Emits model‑level metrics to TimescaleDB. | Writes only via `metrics:write` role. |

All processing nodes run inside a **VPC** with **Zero‑Trust** networking; inter‑service traffic is signed with mTLS.

---

### 4. Storage Tier  
- **Raw Data Lake** – Object storage (S3) with bucket‑level policies; lifecycle rules (90‑day retention).  
- **Processed DB** – PostgreSQL (logical replication) for normalized, validated records.  
- **Model Metrics Store** – TimescaleDB for time‑series of validation scores, drift alerts.  
- **Audit Log Store** – Immutable append‑only log (AWS CloudTrail).  

Encryption‑at‑rest (AES‑256) and **IAM** policies enforce least‑privilege access (e.g., `read:raw`, `write:processed`).

---

### 5. Query / Serving Layer  
| Component | Purpose | Auth / Security |
|-----------|---------|-----------------|
| **Search Service** (ElasticSearch) | Full‑text and faceted search over validation reports. | Role‑based access (`search:read`). |
| **GraphQL API** (Apollo) | Unified query endpoint for UI & external clients. | OAuth2 scopes (`validation:read`). |
| **Cache** (Redis) | Hot data (latest metrics, dashboards). | Network ACLs; auth token required. |
| **Reporting Engine** | Generates PDF/HTML compliance reports. | Runs as a privileged service; output stored in encrypted bucket. |

All endpoints enforce **OAuth2** with short‑lived access tokens; refresh tokens are stored securely in the Auth Service.

---

### 6. Egress to User  
- **Web Dashboard** (React + Auth0) – Authenticated users view validation results, drill‑down into per‑model metrics, receive alerts.  
- **Export API** (REST) – Programmatic access to CSV/JSON reports; supports pagination, filtering.  
- **Webhook / Alerting** – Configurable callbacks (e.g., Slack, PagerDuty) on validation failures or drift detection.  

User authentication is handled by **Auth Service** (OAuth2/OIDC). Each user is assigned roles (`viewer`, `analyst`, `admin`) that map to specific data access permissions enforced at the GraphQL and Export API layers.

---  

### Auth Boundaries Summary  

| Boundary | Enforced By | Typical Tokens / Credentials |
|----------|--------------|------------------------------|
| External → Ingestion | API Gateway + Auth Service | OAuth2 access token (`ingest:*`) |
| Ingestion → Processing | Kafka ACLs + mTLS | Service account JWT (`processor:*`) |
| Processing → Storage | IAM policies + TLS | IAM role (`write:processed`) |
| Storage → Query | DB roles + network ACLs | DB user (`query_user`) |
| Query → Egress (UI/API) | GraphQL/Auth Service | OAuth2 token (`validation:*`) |
| Egress → User | Auth Service + UI session | Session cookie / bearer token |

All traffic is encrypted in‑flight (TLS 1.3) and at‑rest (AES‑256). Auditing is enabled end‑to‑end to satisfy regulatory compliance (HIPAA, GDPR).