# ML Modeling Framing (Credit Decisioning)

## Prediction Targets

We estimate three related outcomes and do not make the final credit decision:

1. **Credit Proxy Score**
   - Estimate the likely bureau score range using lower-cost proxy data before deciding whether to fetch bureau data. This score is not authoritative and cannot be used as the final underwriting basis.

2. **Risk**
   - Estimate expected probability or magnitude of loss, including default, delinquency, charge-off, or fraud-adjusted loss.

3. **Approval Probability**
   - Estimate the probability that the applicant would be approved under the current underwriting policy. This is a policy simulation signal, not the approval decision itself.

---

## Success Metrics

### Model Quality

- Calibration: predicted probabilities match observed outcomes
- PR-AUC / ROC-AUC for risk and approval
- Precision / recall at defined operating thresholds
- Bias / variance monitored across training and production

### Business

- Reduced unnecessary bureau calls
- Higher qualified approval rate
- Lower loss rate at equivalent approval volume
- Decision latency under 300ms for scoring

### Compliance and Explainability

- 99%+ of scored applications have valid reason-code support
- Full auditability of model inputs, features, and versions
- Disparity checks across protected or proxy-sensitive groups
- Drift monitoring by segment and time window
- Review of proxy variables for disparate impact risk

---

## Scope Boundaries

This platform owns:

- Producing proxy score, risk score, and approval probability
- Feature selection, training, validation, and monitoring
- Model serving within latency constraints
- Reason-code generation and explainability artifacts
- Model and feature lineage for audit
- Bureau-fetch recommendation signals (not final decision)

This platform interfaces with:

- Application intake systems
- Feature stores and internal data systems
- Bureau providers
- Underwriting / policy engine (final authority)
- Compliance and audit systems

---

## Non-Goals

This platform does not:

- Make final underwriting decisions
- Define credit policy or approval thresholds
- Assign credit limits or APR
- Own manual review workflows
- Replace compliance or legal review
- Treat proxy score as a substitute for authoritative bureau data

---

## Real-Time Credit Decisioning System Design

### 1. Problem Statement

Design a system that determines whether to approve a customer for credit and under what terms.

Example output:

- Decision: Approved / Declined / Manual Review
- Credit Limit
- APR Tier
- Reason Codes

The system must be fast, reliable, explainable, and auditable.

---

### 2. Functional Requirements

- Accept credit applications in real time
- Fetch external and internal financial data
- Generate ML-based risk and fraud scores
- Apply business and compliance rules
- Return a final decision
- Persist full decision trace for audit
- Emit events for monitoring and analytics

---

### 3. Non-Functional Requirements

- Low latency (sub-second to a few seconds)
- High availability
- Strong auditability and traceability
- Idempotency per application_id
- Security and PII protection
- Model versioning and rollback support

---

### 4. High-Level Architecture

Customer → API → Decision Orchestrator → Data + Models → Rules Engine → Decision → Storage + Events

Detailed flow:

1. Application API
2. Decision Orchestrator
3. Feature Store (online/offline)
4. Model Inference Service
5. Rules Engine
6. Decision Service
7. Audit + Event Pipeline

---

### 5. Core Components

#### Application API

- Validates requests
- Generates application_id
- Enforces idempotency
- Routes request to orchestrator

#### Decision Orchestrator

- Coordinates all downstream calls
- Fetches customer, bureau, fraud, and feature data
- Calls models and rules engine
- Produces final decision

#### Feature Store

- Online: low latency features for inference
- Offline: training and backtesting
- Ensures feature consistency across training and serving

#### Model Inference Service

- Hosts ML models:
  - Credit risk
  - Fraud detection
  - Income verification
- Supports versioning, canary releases, and rollback

#### Reason Code Service

- Generates regulatory-compliant adverse action reason codes
- Consumes:
  - model output (scores / probabilities)
  - feature snapshot used at decision time
  - feature attribution values (e.g., coefficients for linear models, SHAP values for tree models)
  - reason-code mapping version
  - ruleset / policy version
- Produces:
  - top contributing negative factors mapped to approved reason-code categories
- Deterministic and replayable given:
  - model_version
  - feature_snapshot
  - feature-transformation version
  - reason-code logic version
- Does not rely on external services at replay time

Notes:

- ML models (e.g., Logistic Regression, Gradient Boosted Trees) return scores and feature attributions, not regulatory reason codes.
- The Reason Code Service maps feature contributions to standardized, compliant reason codes.

#### Rules Engine

- Applies business and regulatory constraints
- Ensures model outputs comply with policy
- Determines approve / decline / manual review

---

### 6. Decision Flow

1. Request arrives through Application API
2. Idempotency check by application_id / request_id
3. Schema validation rejects unsupported underwriting inputs, including credit_proxy_score
4. Data collection from approved sources (bureau, internal systems, feature store)
5. Feature assembly using versioned feature transformations
6. Persist feature snapshot used for scoring
7. Model inference produces scores, probabilities, and feature attribution values
8. Rules Engine applies underwriting policy and determines approve / decline / manual review
9. Reason Code Service maps feature attributions and policy outcomes to compliant reason codes
10. Persist decision trace, including model_version, ruleset_version, feature_snapshot, feature-transformation version, and reason-code logic version
11. Return decision response from the authorized decisioning path
12. Emit audit and monitoring events for downstream systems

---

### 7. Data Model

#### Application

- application_id
- request_id
- customer_id
- timestamp
- product_type
- channel
- application_status

#### Decision

- decision_id
- application_id
- request_id
- result
- credit_limit
- apr_tier
- reason_codes
- model_versions
- ruleset_version
- reason_code_logic_version
- feature_snapshot_id
- feature_transformation_version
- decision_timestamp

#### Feature Snapshot

- feature_snapshot_id
- application_id
- request_id
- feature_name
- value
- source_system
- source_timestamp
- feature_transformation_version
- feature_store_version

#### Model Artifact

- model_name
- model_version
- artifact_uri
- training_dataset_snapshot_id
- feature_transformation_version
- registered_at
- registered_by
- is_current

#### Reason Code Mapping

- reason_code_logic_version
- feature_name
- attribution_direction
- reason_code
- reason_description
- effective_start_timestamp
- effective_end_timestamp

#### Audit Event

- event_id
- application_id
- request_id
- event_type
- idempotency_key: application_id + request_id + event_type
- step
- timestamp
- service_name
- service_version
- model_name
- model_version
- ruleset_version
- reason_code_logic_version

---

### 8. Reliability and Correctness

Key invariants:

- For any application_id, there is at most one final decision
- Every decision must reference model and ruleset versions
- Decisions must include feature snapshots for audit
- If required data is missing, route to manual review
- Credit Proxy Score must only be stored in audit and observability schemas. It must be explicitly excluded from the underwriting input schema, and any underwriting request containing credit_proxy_score must be rejected at schema validation.
- For each model_name, model_version must be monotonically increasing in the artifact repository. Only one version may be marked current at a time. Rollback changes the current pointer, but does not reuse or mutate version numbers.
- All audit records must be idempotent by application_id + request_id + event_type within a 24-hour rolling dedupe window.
- For any application_id, the decision and adverse action reason codes must be exactly reproducible using the captured model_version, feature_snapshot, feature-transformation version, and reason-code logic version, with deterministic execution and no external dependencies at replay time.
- No automated credit decision may be made using an unapproved, unversioned, expired, or non-replayable model path.

---

### 9. Failure Handling

- Bureau failure → retry or manual review
- Feature store failure → fallback or manual review
- Model failure → use a pre-approved fallback risk model only if it is registered as eligible for fallback, compatible with the current feature schema, and produces compliant reason-code support. If no approved fallback is available, route to manual review rather than auto-decline.
- Duplicate request → return cached decision

#### Degraded Mode Ownership and Response

Decision ownership:

- ML team owns model selection, fallback activation, and system behavior under degradation
- Underwriting owns risk thresholds and approval policy
- Marketing is informed of conversion and volume impact but does not control risk decisions

Immediate system behavior (automatic):

- On detection of fallback model degradation or rising loss signals, shift to conservative decisioning mode:
  - tighten approval thresholds via Rules Engine
  - increase routing to manual review for higher-risk segments
  - optionally suppress approvals in unstable segments

Escalation path:

- ML team investigates model degradation and serving issues
- Underwriting may adjust thresholds or policy bands
- Marketing is notified of expected approval and conversion impact

Invariant:

- The system must never increase loss exposure beyond approved underwriting risk thresholds, even during model degradation or fallback operation

---

### 10. Monitoring

Operational:

- Latency (p50, p95, p99 end-to-end decision time)
- Error rate (% failed requests)
- Throughput (requests per second)
- Dependency failures (timeout/error rate per downstream service)

ML:

- Feature drift (population stability index, PSI)
- Prediction drift (distribution shift vs training baseline)
- Calibration (expected vs actual outcome curves)
- Segment-level approval rate (approval % by cohort)
- Segment-level loss rate (default/charge-off % by cohort)
- Bias/variance tracking (train vs validation vs production performance)

Reasoning / Explainability:

- Reason-code distribution (top N reason codes over time)
- Reason-code stability (variance for same feature patterns)

Business:

- Conversion rate (approved / total applications)
- Loss rate (charge-offs / approved accounts)
- Revenue impact (APR yield, utilization)
- Bureau call rate (% of applications triggering bureau fetch)
- Bureau latency (p95/p99 response time)
- Bureau cost per application

System Behavior:

- Fallback usage rate (% of decisions using fallback model)
- Manual review rate (% routed to human review)
- Conservative mode activation frequency

Fairness / Compliance:

- Disparity ratios across protected or proxy groups (approval rate parity, loss parity)
- Adverse action coverage (% decisions with valid reason codes)

SLOs:

- Decision latency < 300ms (p99)
- Audit write success rate > 99.99%
- Decision reproducibility (100% replay success for audited samples)

---

### 11. Security and Compliance

- Encryption in transit and at rest
- Access controls
- Full audit logging
- Explainable decisions
- Bias and fairness monitoring

---

### 12. Interview Framing

This should be presented as a real-time, regulated decision platform.

Key framing:

- ML is only one component
- System must be explainable and auditable
- Reliability and correctness are critical
- Fail safely to manual review

Tie to experience:

- Large-scale distributed systems
- Streaming data pipelines
- Idempotency and replay
- Reliability under failure
