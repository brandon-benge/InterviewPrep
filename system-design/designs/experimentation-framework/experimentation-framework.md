# Experimentation Framework (A/B Testing Platform)

## Overview
A large-scale experimentation framework enables product teams to run controlled experiments, measure impact, and make data-driven decisions. The system supports feature flags, variant assignment, real-time metric collection, and statistical analysis handling 100M+ users, 500+ concurrent experiments, and 10B events/day.

---

## System Architecture

```mermaid
flowchart TB
    subgraph Client
        A[Web/Mobile Apps]
        C[SDK Library]
    end
    
    subgraph Control Plane
        H[Configuration Service]
        G[(Config DB<br/>PostgreSQL)]
    end
    
    subgraph Data Plane
        D[API Gateway]
        F[Feature Flag Service]
        E[Assignment Service]
        I[(Redis Cache)]
    end
    
    subgraph Event Pipeline
        J[Kafka]
        K[Stream Processor<br/>Flink/Spark]
        L[Batch Processor<br/>Airflow]
    end
    
    subgraph Storage & Analysis
        M[(Data Warehouse<br/>Snowflake/BigQuery)]
        N[(OLAP DB<br/>Druid)]
        O[Statistical Analysis]
        P[Metric Aggregation]
    end
    
    subgraph UI
        Q[Experiment Dashboard]
    end
    
    A --> C
    C --> D
    D --> F
    F --> H
    F --> E
    E <--> I
    H --> G
    Q --> H
    C --> J
    J --> K
    J --> L
    K --> N
    L --> M
    P --> M
    P --> N
    O --> M
    Q --> O
    Q --> P
```

---

## Core Components

### 1. Feature Flag Service
**Purpose:** Orchestrates experiment evaluation and config bundle generation

**Capabilities:**
- Boolean/multivariate flags
- Gradual rollout (0% → 10% → 50% → 100%)
- Instant rollback (kill switch)
- User targeting (whitelist, segments)
- **Config bundle download** for SDK initialization
- **Offline evaluation** via cached bundles (no network calls)

**SDK Initialization Flow:**
1. App starts → SDK calls `GET /config-bundle?user_id=12345`
2. Service calls Configuration Service to get active experiments and flag mappings
3. Service calls Assignment Service to compute variants for this user
4. Service pre-computes all flag assignments and returns bundle
5. SDK caches bundle locally (in-memory or disk)
6. Code queries flags instantly via local lookup: `sdk.getVariant('checkout_button_color')` → `'red'`
7. SDK refreshes bundle periodically (30s-5min) or on app restart

**Tech:** Custom service or LaunchDarkly/Split.io

### 2. Configuration Service (Control Plane)
**Purpose:** Manages experiment metadata and feature flag definitions
- Experiment setup (variants, traffic allocation, metrics, duration)
- Feature flag rules (targeting, rollout %, kill switches)
- **Flag-to-Experiment mapping** (e.g., `checkout_button_color` → `exp_checkout_v2`)
- Version control and audit history
- Config bundle publishing for offline evaluation

**Storage:** PostgreSQL with versioning
**API:** REST endpoints for CRUD operations with RBAC

**Key Insight:** Developers reference **flag keys** in code (e.g., `checkout_button_color`), not experiment IDs. Configuration Service maintains the mapping to active experiments.

### 3. Assignment Service (Data Plane)
**Purpose:** Determines variant assignment for users

**Assignment Algorithm:**
- Deterministic hashing: `Hash(user_id + experiment_id) % 100`
- Ensures consistency across sessions/devices
- Independent experiments via separate hash spaces
- Sticky assignments (user never switches variants)

**Performance:** <10ms p99 latency via Redis cache
**Deployment:** Multi-region for low latency

**Example:**
```
User: 12345, Experiment: exp_checkout_v2
Hash("12345_exp_checkout_v2") % 100 = 37
Split: Control (0-49), Treatment (50-99) → Control
```

### 4. Event Pipeline
**Purpose:** Captures exposures and user behavior

**Event Types:**
- Exposure: User saw variant
- Metric: User action (click, purchase, signup)
- Diagnostic: Errors, latency

**Flow:** `Client SDK → API Gateway → Kafka → Flink (real-time) + Spark (batch) → Data Warehouse`

**Schema:**
```json
{
  "event_type": "exposure",
  "user_id": "12345",
  "experiment_id": "exp_checkout_v2",
  "variant": "treatment",
  "timestamp": "2025-12-04T10:30:00Z",
  "context": {"platform": "web", "device": "desktop"}
}
```

**Scale:** 10B events/day (100K/sec peak), Kafka 1000 partitions by user_id

### 5. Metric Aggregation & Statistical Analysis
**Purpose:** Transform events into experiment results

**Aggregation:**
- Pre-aggregate daily user-level metrics (speeds queries by 100x)
- Store in Data Warehouse (Snowflake) and OLAP DB (Druid)
- Real-time dashboards (5min lag) + batch analysis (daily)

**Statistical Methods:**
- Frequentist: t-test, chi-square, confidence intervals
- Bayesian: Posterior distributions (optional view)
- Sequential testing: Early stopping with alpha spending

**Outputs:** P-value, effect size, MDE, power, sample size

### 6. Dashboard
**Purpose:** Experiment creation, monitoring, and decision-making

**Features:**
- Configure experiments (no-code)
- Real-time results with trend charts
- Segmentation (platform, country, cohort)
- Launch controls (ship, iterate, kill)

**Tech:** React + D3.js + REST API

---

## Data Flow Example: Checkout Button Experiment

### 1. Setup (Configuration Service)
PM creates experiment via dashboard:
```json
{
  "experiment_id": "exp_checkout_v2",
  "flag_key": "checkout_button_color",
  "variants": {"control": "green", "treatment": "red"},
  "traffic_allocation": 50,
  "duration": "7 days",
  "primary_metric": "conversion_rate"
}
```

### 2. SDK Initialization (App Startup)
User 12345 opens app → SDK initializes:
```javascript
await sdk.initialize({userId: "12345"});
// SDK calls: GET /config-bundle?user_id=12345
// Response includes pre-computed assignments for all active flags
```

Config bundle returned:
```json
{
  "flags": [
    {
      "key": "checkout_button_color",
      "experiment_id": "exp_checkout_v2",
      "variant": "red",
      "in_experiment": true
    }
  ]
}
```
SDK caches bundle locally for instant lookups.

### 3. Feature Evaluation (Checkout Page)
Developer code queries flag by key:
```javascript
const buttonColor = sdk.getVariant('checkout_button_color');
// Instant local lookup from cached bundle: 'red'
// No network call!

<button style={{backgroundColor: buttonColor}}>Complete Purchase</button>
```

### 4. Exposure Logging (Automatic)
SDK automatically logs exposure when flag is queried:
```json
{
  "event_type": "exposure",
  "user_id": "12345",
  "flag_key": "checkout_button_color",
  "experiment_id": "exp_checkout_v2",
  "variant": "red",
  "timestamp": "2025-12-04T10:30:00Z"
}
```
Event sent asynchronously to Kafka (non-blocking).

### 5. User Action (Metric Logging)
User completes purchase → SDK logs metric:
```javascript
sdk.track('purchase', {amount: 99.99});
```
```json
{
  "event_type": "purchase",
  "user_id": "12345",
  "amount": 99.99,
  "timestamp": "2025-12-04T10:31:00Z"
}
```

### 6. Analysis (Aggregation Service)
Spark joins exposure + purchase events by user_id:
- Control: 1000 users, 150 conversions (15%)
- Treatment: 1000 users, 180 conversions (18%)
- Statistical test: p-value = 0.03 (significant at 95%)
- Dashboard shows: **+20% relative lift**

### 7. Decision
PM reviews results → Ships red button to 100% via dashboard (no code deployment needed).

---

**Key Takeaways:**
- Developer never sees experiment ID, only flag key (`checkout_button_color`)
- SDK downloads config bundle once on startup (not per-request)
- Flag evaluation is instant (local cache lookup, <1ms)
- Exposure logging is automatic and asynchronous
- Config changes propagate on next SDK refresh (30s-5min delay)

---

## Design Decisions & Trade-offs

### Consistent Hashing for Assignment
**Why:** Same user always sees same variant (prevents bias)
**Trade-off:** Cannot rebalance traffic mid-experiment

### Fire-and-Forget Event Collection
**Why:** Low latency (<10ms), acceptable <0.1% loss
**Trade-off:** Some events lost; use idempotency keys for retries

### Pre-aggregated Metrics
**Why:** Query time: seconds vs minutes
**Trade-off:** Raw events kept 90 days for ad-hoc analysis

### Multi-Region Data Plane
**Why:** <10ms assignment latency globally
**Approach:** Config propagated via pub/sub every 30s, local Redis cache per region

---

## Scale Considerations

**Throughput:**
- 100M DAU, 500 concurrent experiments
- 10B events/day (100K/sec peak)
- 1M assignment requests/sec

**Performance Targets:**
- Assignment: <10ms p99
- Event ingestion: <100ms end-to-end
- Dashboard queries: <5 seconds

**Scaling:**
- **Assignment:** Redis cluster, consistent hash partitioning, regional deployment
- **Events:** Kafka 1000 partitions, Flink autoscaling, batched warehouse writes (10K rows)
- **Warehouse:** Partition by date + experiment_id, materialized views, rollup tables

---

## Advanced Features

### Mutual Exclusion Groups
**Problem:** Multiple experiments on same surface cause interference
**Solution:** Define exclusion groups (e.g., "checkout_page"); only 1 active per user

### Holdout Groups
**Problem:** Measure long-term cumulative impact
**Solution:** Reserve 5-10% users who never see treatments; compare over 3-6 months

### Multi-Armed Bandits
**Problem:** Traditional A/B tests slow (fixed duration)
**Solution:** Thompson Sampling dynamically allocates traffic to best variant
**Use Case:** Content recommendation, ad optimization

### Heterogeneous Treatment Effects
**Problem:** Treatment works for some segments, not others
**Solution:** Subgroup analysis + CATE models

---

## Common Pitfalls & Mitigations

| Pitfall | Detection | Mitigation |
|---------|-----------|------------|
| **Sample Ratio Mismatch (SRM)** | Chi-square test (alert if p<0.01) | Fix assignment bugs, check client-side filtering |
| **Peeking (multiple testing)** | Track query frequency | Set fixed duration, use sequential testing |
| **Novelty effect** | Monitor metric decay over time | Run 2-4 weeks minimum |
| **Carryover effects** | Historical exposure correlation | Washout period between experiments |

---

## Monitoring & Observability

**Key Metrics:**
- Assignment: Latency, cache hit rate, error rate
- Events: Kafka lag, loss rate, throughput
- Experiments: SRM rate, exposure coverage, guardrail violations

**Alerts:**
- SRM: Control/treatment ratio deviates >5%
- Guardrail: Revenue/errors degrade significantly
- Pipeline lag: Kafka lag >5 minutes

**Dashboards:**
- System health (uptime, latency)
- Experiment health (active count, sample sizes)
- Data quality (schema failures, duplicates)

---

## Security & Privacy

**Access Control:**
- Experiment config: Product/eng teams only
- Raw events: Data team only (audited)
- Aggregate results: All employees (no PII)

**GDPR Compliance:**
- Right to erasure: Anonymize user_id after deletion
- Consent: Only run experiments on consented users
- Retention: Raw events 90 days, aggregates 2 years

**Anonymization:**
- Store SHA256(user_id) in warehouse
- Differential privacy for sensitive metrics (optional)

---

## Identity & Stickiness

**User Types:**
- Logged-in: Use `user_id` (preferred)
- Anonymous: Generate `anonymous_id` in SDK, migrate on login
- Device: Use `device_id` for IoT/edge

**Stickiness:** Same user always sees same variant via deterministic hashing

---

## API Surface

### Client/SDK APIs
- `POST /evaluate` – Get variant for flag + user context
- `GET /config-bundle` – Download config for offline evaluation
- `POST /exposures` – Log exposure events
- `POST /metrics` – Log behavior events

### Admin APIs
- `POST /flags`, `PATCH /flags/{key}` – Manage feature flags
- `POST /experiments`, `PATCH /experiments/{id}` – Manage experiments
- `GET /flags/{key}/history`, `POST /flags/{key}/rollback` – Version control

---

## Failure Modes & Mitigations

| Failure | Impact | Mitigation |
|---------|--------|------------|
| Control plane down | Cannot edit flags | Evaluation continues via cached bundles |
| Redis outage | Assignment latency | Fallback to DB + multi-node cluster |
| Kafka lag | Delayed metrics | Autoscaling consumers, alerts |
| SRM detected | Invalid experiment | Auto-pause experiment |
| Bad rollout | Wrong UI shown | Instant rollback via control plane |

---

## Tech Stack

| Component | Options |
|-----------|---------|
| **Config Storage** | PostgreSQL, MongoDB |
| **Cache** | Redis, Memcached |
| **Event Stream** | Kafka, Pulsar, Kinesis |
| **Stream Processing** | Flink, Spark Streaming, Kafka Streams |
| **Batch Processing** | Spark, Airflow |
| **Data Warehouse** | Snowflake, BigQuery, Redshift |
| **OLAP DB** | Druid, ClickHouse |
| **Feature Flags** | LaunchDarkly, Split.io, Unleash |
| **Stats** | Python (SciPy, statsmodels), R |
| **Dashboard** | React + D3.js, Tableau, Looker |

---

## References

- Kohavi, Ron. "Trustworthy Online Controlled Experiments" (A/B Testing at Scale)
- Netflix TechBlog: Experimentation Platform
- Uber Engineering: XP Platform Architecture
- Facebook Research: Adaptive Experimentation with Thompson Sampling
- Google: ExP Platform Design

---

## Summary

**Key Components:**
1. Assignment Service (consistent hashing, <10ms)
2. Feature Flag Service (instant rollout/rollback)
3. Event Pipeline (Kafka → Flink/Spark → Warehouse)
4. Metric Aggregation (pre-computed stats)
5. Statistical Analysis (t-tests, confidence intervals)
6. Dashboard (no-code experiment creation)

**Critical Success Factors:**
- **Reliability:** Assignment bugs corrupt experiments (invest in testing)
- **Speed:** <10ms assignment, <5min metric lag
- **Accuracy:** Detect SRM, control multiple testing
- **Usability:** Non-technical PMs launch experiments independently

**Scale:** 100M+ users, 500+ concurrent experiments, 10B events/day
