# customer-journey.md  

## Medic‑Verify – Customer Journey Map  

| Phase | Trigger Event | Friction Points | User Emotions | Opportunities to Delight | Success Metric |
|------|---------------|----------------|---------------|--------------------------|----------------|
| **Aware** | • Publication of a regulatory warning (e.g., FDA draft guidance) on AI model drift in radiology.<br>• Attendance at a “AI in Healthcare” conference where a speaker cites recent failures of AI‑driven triage tools. | • Over‑abundance of generic AI‑validation tools that don’t address HIPAA/clinical‑workflow constraints.<br>• Lack of clear terminology (“reliability validation”) in existing marketing material. | Curiosity → Anxiety (risk of non‑compliance) | • Publish a concise “Healthcare AI Reliability Checklist” (1‑page PDF) that references the regulatory warning.<br>• Run a targeted LinkedIn carousel ad with the headline: “Is your AI safe enough for the clinic? 3 red‑flags you can’t ignore.” | **Impression‑to‑Click Rate** – target ≥ 2.5 % on ad; **PDF download** – ≥ 150 downloads per webinar. |
| **Consider** | • Decision‑maker (Chief Medical Officer, Head of AI) receives the checklist and schedules a 30‑min demo after seeing a case study of a radiology AI vendor that avoided a $2 M recall using Medic‑Verify. | • Uncertainty about integration effort with existing PACS/EHR.<br>• Concern over data‑privacy (PHI) during validation runs.<br>• Limited internal expertise to interpret reliability metrics. | Interest → Skepticism | • Offer a **sandbox environment** pre‑loaded with de‑identified DICOM data and a step‑by‑step “One‑click reliability report” wizard.<br>• Provide a **Compliance Companion** PDF mapping Medic‑Verify outputs to FDA, EMA, and ISO 14971 requirements.<br>• Assign a dedicated **Solution Engineer** for a live walkthrough. | **Demo‑to‑Trial Conversion** – target ≥ 45 %; **Time to First Report** in sandbox ≤ 15 min. |
| **Try** | • Customer signs a 30‑day pilot (no‑credit‑card) to run Medic‑Verify on their in‑house AI model (e.g., sepsis early‑warning). | • Pilot onboarding time (data ingestion, environment provisioning).<br>• Need to calibrate reliability thresholds for different clinical use‑cases.<br>• Potential false‑positive alerts during stress‑testing. | Anticipation → Frustration (if onboarding stalls) | • **Rapid‑Onboard Kit**: automated data‑pipeline scripts that ingest HL7/FHIR streams within 2 hours.<br>• **Threshold‑Assist AI** that suggests clinically‑reasonable reliability thresholds based on historical performance.<br>• 24/7 **Pilot Support Slack channel** with SLA ≤ 30 min response. | **Pilot Completion Rate** – target ≥ 90 % (≥ 1 reliable report generated).<br>**Time‑to‑Value** – median ≤ 3 days from kickoff to first actionable insight. |
| **Adopt** | • Pilot demonstrates a 22 % reduction in model drift incidents and a 15 % faster regulatory audit (internal audit team). | • Negotiating enterprise licensing (price, seat count).<br>• Integrating Medic‑Verify into CI/CD pipelines for continuous validation. | Confidence → Excitement | • Offer **Enterprise Bundle** with volume discounts (e.g., 10‑seat tier at 20 % off).<br>• Provide **CI/CD Plug‑ins** for Jenkins, GitHub Actions, and Azure DevOps that auto‑run reliability suites on each model push.<br>• Include **Quarterly Health‑Check** webinars reviewing trends across all validated models. | **Close‑Rate** – target ≥ 55 % of pilots convert to paid contracts.<br>**Annual Recurring Revenue (ARR) per account** – aim ≥ $120k (mid‑size hospital). |
| **Expand** | • Customer adds new AI modules (e.g., pathology image analysis) and requests cross‑model reliability dashboards. | • Scaling to multi‑site deployments; data‑governance across jurisdictions (US vs EU).<br>• Need for custom compliance reports for audits. | Satisfaction → Advocacy | • Roll out **Multi‑Site Federation** feature that aggregates reliability metrics across hospitals while preserving data locality.<br>• Enable **Custom Report Builder** with drag‑and‑drop sections for ISO, FDA, and internal governance.<br>• Launch a **Customer Advisory Board** (CAB) with early‑access to new features and co‑marketing opportunities. | **Expansion Rate** – target ≥ 30 % of accounts add ≥ 1 additional model within 12 months.<br>**Net Promoter Score (NPS)** – aim ≥ 70. |

---  

### Narrative Flow (High‑Level)

1. **Aware** – Regulatory alerts create a sense of urgency; we capture attention with a checklist and concise ad copy.  
2. **Consider** – Decision‑makers evaluate fit; we reduce perceived risk with sandbox demos, compliance mapping, and personal engineering support.  
3. **Try** – A friction‑free pilot proves the platform’s value; rapid onboarding and AI‑assisted thresholding keep momentum high.  
4. **Adopt** – Demonstrated ROI drives contract negotiations; enterprise bundles and CI/CD integration cement the partnership.  
5. **Expand** – Cross‑model, multi‑site capabilities and co‑creation programs turn satisfied customers into advocates and growth engines.  

---  

### Key Assumptions & Numbers  

- **Target Market**: 1,200 US hospitals + 300 EU health systems actively deploying AI (2025 data).  
- **Conversion Funnel**: 10 % of aware → consider, 45 % of consider → try, 55 % of try → adopt, 30 % of adopt → expand.  
- **Revenue Forecast (Year 1)**: 30 pilots → $120k ARR each = **$3.6 M**; expansion adds another **$1.1 M**.  

---  

*Prepared by Business‑Synthesis – Medic‑Verify*