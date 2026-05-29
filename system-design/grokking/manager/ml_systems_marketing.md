# ML System Design: Credit Product Recommendation and Personalization

## Scenario

Design a machine learning system for a financial services company that recommends the best eligible credit product to a customer across channels such as email, mobile app, and web.

The business goal is to improve qualified offer conversion, approval likelihood, and long-term customer value while controlling credit risk, fraud risk, fairness risk, and regulatory exposure.

This is a recommendation and ranking system. It should influence which eligible product is shown to a customer, but it should not replace final underwriting or credit policy decisions.

---

## 1. Problem Framing

### Prediction Targets

We are not predicting one thing. We are estimating four related outcomes:

1. **Response / acceptance probability**
   - How likely is the customer to respond to or accept the offer?

2. **Approval probability**
   - How likely is the customer to be approved under the current underwriting policy?

3. **Expected long-term value**
   - If approved, what is the expected long-term value of this customer-product relationship?

4. **Expected risk or loss**
   - What is the expected probability or magnitude of loss, such as default, delinquency, charge-off, or fraud?

The recommendation layer should rank products using these estimates, but final eligibility and underwriting decisions remain owned by credit policy and underwriting systems.

---

## 2. Success Metrics

### ML Metrics

- **PR-AUC**
  - Useful for imbalanced outcomes such as response, approval, fraud, default, or charge-off.

- **Calibration**
  - A predicted `70%` approval probability should be close to a real-world `70%` approval rate.

- **Precision at fixed recall / recall at fixed precision**
  - Use this when the business wants to either avoid bad offers or expand reach while maintaining a quality threshold.

- **Slice-level performance**
  - Validate performance by product, channel, customer segment, credit band, geography, and customer tenure.

### Business Metrics

- Higher qualified offer conversion rate.
- Higher approval rate among targeted customers.
- Higher expected long-term value.
- Stable or improved loss rate.
- No increase in compliance, fairness, or reputational risk.

### Fairness and Compliance Metrics

- Disparity checks across protected or proxy-sensitive groups.
- Adverse-action explainability where applicable.
- Drift monitoring by segment and time window.
- Ongoing review for proxy variables that could create disparate impact.

---

## 3. Scope Boundaries and Non-Goals

### In Scope

- Recommend and rank eligible credit products for a customer.
- Use approved customer, bureau, marketing, product, and macroeconomic features.
- Score candidate products across channels.
- Produce auditable model outputs, reason codes, and lineage.
- Monitor performance, drift, fairness, and calibration over time.

### Out of Scope

- Final underwriting decisions.
- Credit policy definition.
- Regulatory rule definition.
- Adverse action ownership.
- Manual override workflows.
- Changing legal or compliance standards.

The recommendation system may consume eligibility constraints from underwriting, but it must not override them.

---

## 4. Correctness Invariants

These are non-negotiable contracts for the system.

1. **Point-in-time correctness**
   - Every training and serving feature must have been available at the time the recommendation would have been made.

2. **No leakage**
   - The model must not train on post-decision outcomes, future data, or the same examples used for unbiased validation.

3. **Fairness and compliance**
   - The system must not use protected attributes or obvious proxy variables in ways that create unlawful disparate impact.

4. **Lineage and repeatability**
   - Every recommendation must be reproducible from the model version, feature values, data snapshot, feature definitions, and policy version.

5. **Underwriting boundary**
   - The recommendation system can rank eligible products, but it must not override underwriting eligibility or credit policy.

6. **Decision traceability**
   - Every delivered or suppressed recommendation must reference the model version, ruleset version, feature snapshot, and request context used to produce it.

7. **One decision per placement**
   - For a given request and placement, the system returns at most one final selected action.

8. **Fail-safe behavior**
   - If customer context, consent, or eligibility cannot be determined, the system must fail closed and avoid showing a product offer.

9. **Suppression explainability**
   - A suppressed recommendation must carry a suppression reason for audit, debugging, and customer-protection review.

---

## 5. Data Sources

### Candidate Data Sources

- Customer profile data.
- Credit bureau attributes.
- Prior marketing exposure and response history.
- Product catalog and product eligibility rules.
- Prior application and approval outcomes.
- Account performance history.
- Fraud history.
- Macroeconomic context such as rates, inflation, unemployment, or broader credit conditions.

### Data to Treat Carefully or Exclude

- Protected attributes such as race, gender, or age.
- Proxy-sensitive variables such as zip code, education, or other geography and socioeconomic indicators.
- Stale, unmaintained, or poorly sourced features.
- User-declared data that is not verified or not approved for the use case.
- Post-decision signals, including:
  - Approval result.
  - Credit line assigned.
  - Account activity after approval.
  - Collections activity.
  - Future fraud outcomes.
  - Future payment behavior.

### Income Handling

Income should not be treated as automatically trusted or real-time. It may be relevant, but it must be governed carefully.

A production system should treat income as:

- **Verified** through approved sources such as bureau data, user verification, payroll integrations, document verification, or bank transaction analysis.
- **Current enough** based on feature freshness rules and timestamps.
- **Explainable** with a clear source, feature definition, and reason-code strategy.
- **Policy-approved** for the specific use case, such as marketing, eligibility, underwriting, or servicing.
- **Compliant** with fair lending and model risk requirements.

Interview phrasing:

> Income is not truly real-time. I would rely on last-known verified or modeled income with strict point-in-time tracking, freshness constraints, and governance approval. It must be explainable, auditable, and pass fairness checks. In some cases, it may be transformed or excluded depending on compliance requirements.

---

## 6. System Architecture and Online Decision Flow

### Functional Requirements

- Ingest customer and system events from app, web, email, call center, transaction, application, and response systems.
- Build point-in-time customer context from historical and real-time behavior.
- Generate candidate credit products or safe fallback actions.
- Filter candidates using eligibility, consent, suppression, compliance, and risk-policy rules.
- Rank eligible candidates in real time.
- Return a decision with lineage, reason codes, and suppression details.
- Capture impressions, clicks, application starts, approvals, conversions, complaints, opt-outs, and later credit outcomes.
- Support experimentation, replay, and audit.

### Non-Functional Requirements

- Low-latency serving for app and web channels.
- High availability for customer-facing decisioning.
- Strict privacy and consent enforcement.
- Reproducible decisions for audit and debugging.
- Training-serving consistency across feature definitions.
- Safe rollback and champion/challenger deployment patterns.
- Scalable event processing across millions of customers and interactions.

### High-Level Architecture

```text
Customer / Bureau / Marketing / Product / Macro Data
                    ↓
             Event Ingestion
                    ↓
     Shared Point-in-Time Feature Platform
           ↓                         ↓
 Offline Feature Store         Online Feature Store
           ↓                         ↓
     Model Training        Recommendation / Decision API
                                     ↓
                           Customer Context Service
                                     ↓
                             Candidate Generator
                                     ↓
                    Eligibility / Consent / Policy Filter
                                     ↓
                           Ranking and Decisioning
                                     ↓
                            Channel Activation
                                     ↓
                      Feedback, Monitoring, Audit
```

### Online Serving Flow

1. Customer opens app, visits the website, or becomes eligible for a channel-triggered campaign.
2. Recommendation API receives a request with customer, channel, placement, and session context.
3. Customer context service loads governed state such as product ownership, prior exposure, consent, and current account status.
4. Online features are fetched using the same canonical definitions used in offline training.
5. Candidate generator creates eligible credit-product candidates and safe fallback actions such as no offer.
6. Eligibility, compliance, consent, suppression, and risk-policy filters remove invalid options.
7. Ranking models estimate response, approval, risk, and long-term value signals.
8. Decision engine applies business policy and chooses the final action.
9. Channel activation returns the selected product or suppresses the placement.
10. Impression, click, application, approval, conversion, complaint, opt-out, and later account-performance events flow back for training and monitoring.

---

## 7. Core Platform Components

### Event Ingestion

Captures customer and system events such as:

- app login
- page view
- product browse
- email open
- offer click
- application start
- application complete
- approval
- conversion
- opt-out

Implementation patterns:

- Kafka or Kinesis for streaming ingestion.
- Schema registry for event contracts.
- Replay support for backfills and model reprocessing.
- Dead-letter queues for malformed events.

### Customer Context Service

Builds the governed view of the customer used during decisioning.

Typical inputs:

- existing products
- recent account activity
- prior applications and approvals
- recent offer exposure
- consent and channel preferences
- fraud or support state
- credit-policy eligibility outputs

This service should return normalized, approved context rather than raw sensitive data whenever possible.

### Feature Platform

The feature platform should separate storage by serving need, but keep definitions shared.

```text
1. Offline features  → training, backtesting, experimentation
2. Online features   → low-latency serving
3. Shared definitions → one canonical definition layer used by both
```

This avoids train/serve skew.

Example:

```text
Training definition:
travel_spend_90d = posted travel transactions over last 90 days

Serving definition:
travel_spend_90d = pending + posted travel transactions over last 90 days
```

If those differ, production predictions become unreliable even if offline metrics looked strong.

Typical offline features:

- spend by category over 30, 60, and 90 days
- product ownership history
- prior campaign impressions and response history
- bureau-derived credit attributes
- account performance history
- modeled long-term value

Typical online features:

- current session behavior
- most recent transaction or app interaction
- recent offer suppression state
- current channel and device
- current fraud or support state
- freshness-aware eligibility indicators

Typical shared feature requirements:

- versioned
- point-in-time safe
- reproducible
- discoverable
- tied to lineage and tests

### Candidate Generation

Generates the credit products or safe fallback actions that can be considered for ranking.

Examples:

- travel rewards card
- cash back card
- balance transfer card
- secured card
- no offer

This stage should be broad and fast. It narrows the search space before expensive ranking.

### Eligibility, Consent, and Compliance Filter

Removes candidates that should not be shown.

Examples:

- customer is not eligible for the product
- customer already has the product
- channel consent is missing
- frequency cap has been reached
- fraud or support state requires suppression
- required disclosure is unavailable
- risk policy blocks the offer

The system should rank only eligible candidates. It must not use ML to bypass policy controls.

### Ranking and Decision Engine

The ranking layer estimates signals such as:

- response likelihood
- approval likelihood
- expected risk or loss
- expected long-term value

The decision engine then combines those signals with business policy, trust safeguards, and channel rules to choose the final action.

### Channel Activation

Delivers the final decision to:

- mobile app
- web
- email
- SMS
- push notification
- call-center tooling

Each channel has different latency, formatting, and consent constraints.

### Feedback Loop

Every recommendation should generate feedback events that flow into:

- offline training data
- model evaluation
- experimentation
- suppression logic
- business reporting

Important events include impression, click, application start, application complete, approval, conversion, complaint, opt-out, delinquency, and loss outcomes.

---

## 8. Runtime Data Model, Reliability, and Monitoring

### Core Runtime Records

- Recommendation request
  - `request_id`, `customer_id`, `channel`, `placement`, `session_id`, `request_timestamp`, `context_version`

- Recommendation decision
  - `decision_id`, `request_id`, `customer_id`, `selected_product`, `ranking_model_version`, `ruleset_version`, `feature_snapshot_id`, `reason_codes`, `suppression_reason`, `created_at`

- Candidate record
  - `candidate_id`, `request_id`, `product_id`, `eligibility_status`, `model_score`, `rank`, `filter_reason`

- Feature snapshot
  - `feature_snapshot_id`, `customer_id`, `feature_name`, `feature_value`, `feature_version`, `source_timestamp`

- Feedback event
  - `feedback_event_id`, `decision_id`, `customer_id`, `event_type`, `event_timestamp`, `channel`, `metadata`

### Failure Handling

- Online feature store timeout
  - Use a safe fallback if policy allows, otherwise return no offer.

- Ranking model unavailable
  - Fallback to previous stable model version, rules-only ranking, or no offer depending on risk policy.

- Eligibility service unavailable
  - Fail closed. Do not show a product offer.

- Event ingestion failure
  - Buffer, retry, and route malformed events to a dead-letter queue.

- Duplicate request
  - Use request and placement identifiers to dedupe and avoid duplicate impressions.

- Downstream channel failure
  - Record delivery failure and do not count it as an impression.

### Monitoring

Operational metrics:

- recommendation latency
- API error rate
- feature store latency
- model inference latency
- eligibility service failures
- event ingestion lag
- dead-letter queue volume
- decision throughput

ML metrics:

- feature drift
- prediction drift
- calibration by segment
- model quality by product and channel
- approval, response, and loss performance by segment

Business metrics:

- application starts
- completed applications
- approval rate
- funded accounts
- conversion lift
- long-term value
- loss rate
- complaint and opt-out rate

Trust and safety metrics:

- suppressed recommendation rate
- frequency-cap violations
- consent violations
- fairness metrics
- adverse customer experience signals

### Experimentation and Security

Experimentation support:

- A/B testing of ranking models and policies.
- Champion/challenger comparisons.
- Measurement of long-term value, not just click-through rate.
- Replay and backtesting using stored requests, decisions, and feature snapshots.

Security, privacy, and compliance controls:

- Encrypt data in transit and at rest.
- Restrict access to PII and sensitive financial attributes.
- Enforce consent and communication preferences.
- Tokenize or minimize sensitive data where possible.
- Keep full audit trails of delivered and suppressed decisions.
- Support retention and deletion requirements.

---

## 9. Train / Validation / Test Strategy

Avoid a simple random split because customer behavior, credit policy, economic conditions, and marketing strategy change over time.

Use a forward-looking time-based split:

```text
Train           Oldest historical window
Validation      Later window for features, thresholds, and hyperparameters
Test            Later unseen window for final pre-launch evaluation
OOT Holdout     Most recent unseen period for temporal robustness
```

The out-of-time holdout is especially important because it checks whether the model generalizes to a newer regime.

### Required Slice Validation

Validate by:

- Product.
- Channel.
- Customer segment.
- Credit band.
- Geography.
- Customer tenure.
- Risk band.
- Marketing cohort.

### Biggest Data Risks

- Historical selection bias.
- Delayed labels.
- Leakage.
- Sparse data.
- Distribution drift.
- Class imbalance.
- Train/serve skew.
- Optimizing a proxy metric instead of true business value.

---

## 10. Model Choice

### Recommended Model Families by Target

| Target | Model Family | Notes |
|---|---|---|
| Response / acceptance | Ranking model or gradient boosted trees per product/channel | Useful when ranking multiple candidate offers. |
| Approval probability | Logistic regression baseline, then constrained gradient boosted trees if explainability allows | Approval models require strong explainability and calibration. |
| Risk / loss | Logistic regression or gradient boosted trees | Must include calibration, fairness testing, and strong governance. |
| Long-term value | Supervised regression, survival model, or uplift / causal model | Time series may help with macro or portfolio forecasting, but customer-level LTV is usually supervised learning. |

### When to Choose Each Model

#### Logistic Regression

Use when:

- You need a simple, interpretable baseline.
- The target is binary classification on structured data.
- Regulatory explainability matters.
- You need stable reason codes and easier governance.

#### Gradient Boosted Trees

Use when:

- The problem is tabular and structured.
- You need strong predictive performance.
- Nonlinear relationships and feature interactions matter.
- The model can still meet explainability and governance requirements.

Common examples:

- Fraud prediction.
- Credit risk.
- Churn prediction.
- Approval likelihood.
- Response likelihood.

#### Recommendation / Ranking Models

Use when:

- The goal is to rank multiple candidate products, offers, or actions.
- The question is not simply yes/no.
- The output is an ordered list of options.

Examples:

- Which card should be shown first?
- Which offer should be prioritized?
- Which channel and message should be used?

---

## 11. Handling Class Imbalance

Class imbalance is common in fraud, default, charge-off, and response prediction.

Common approaches:

- Oversample the minority class.
- Undersample the majority class.
- Use class weights.
- Tune the decision threshold.
- Evaluate with precision, recall, F1, and PR-AUC instead of raw accuracy.
- Review performance by segment so minority group performance does not get hidden by aggregate metrics.

Interview phrasing:

> I would not rely on accuracy for imbalanced outcomes. I would use PR-AUC, precision and recall at business-relevant thresholds, class weighting or sampling if needed, and segment-level validation to make sure the model performs safely across customer cohorts.

---

## 12. Explainability and Governance

The model must remain usable in a regulated financial environment.

Approach:

- Start with the most interpretable model that can meet the business target.
- Use logistic regression or constrained tree-based models as strong baselines.
- Use explainable, approved features.
- Document the training data, feature definitions, and model logic.
- Produce reason codes where decisions affect eligibility, approval, or adverse-action-sensitive outcomes.
- Monitor drift, calibration, and fairness over time.
- Only adopt a more complex model if the performance gain clearly justifies the additional governance burden.

Interview phrasing:

> I would trade off some model complexity for explainability and regulatory safety. In this domain, a slightly less accurate model that is explainable, stable, and compliant may be better than a higher-performing black-box model that cannot be governed safely.

---

## 13. Pre-Launch Validation and Release Readiness

Before release, I would require:

1. **Validation metrics**
   - PR-AUC, calibration, precision/recall at threshold, and slice-level performance.

2. **Test-window evaluation**
   - Evaluate on later time windows that were not used for training or tuning.

3. **Out-of-time holdout results**
   - Confirm temporal robustness against drift and changing economic conditions.

4. **Fairness and compliance review**
   - Confirm protected attributes and proxy-sensitive variables are handled appropriately.

5. **Leakage review**
   - Confirm all features are point-in-time correct and exclude post-decision signals.

6. **Model artifacts**
   - Persist model binary, metadata, feature list, feature definitions, training dataset snapshot, and model card.

7. **Experiment tracking**
   - Record:
     - Experiment name.
     - Owner.
     - Dataset version.
     - Feature definitions.
     - Code version.
     - Hyperparameters.
     - Model artifact location.
     - Offline metrics.
     - Validation slices by segment.
     - Notes.
     - Approval status.

8. **Shadow or champion/challenger evaluation**
   - Compare the new model against the current baseline before full rollout.

---

## 14. Bias / Variance Checks

### Overfitting / High Variance

A model may be overfit if:

- Training performance is strong.
- Validation or test performance is materially worse.
- Segment performance is unstable.
- Performance changes significantly across time windows or cohorts.

Meaning:

> The model learned patterns specific to the training data instead of stable generalizable signal.

### Underfitting / High Bias

A model may be underfit if:

- Training and validation performance are both weak.
- The model is too simple.
- Important features are missing.
- The model cannot capture the true signal.
- Error is systematic across many slices.

Meaning:

> The model is not expressive enough or does not have enough useful signal to solve the problem well.

### Performance Means Model Quality

In this context, performance means model quality, not speed.

Examples:

- PR-AUC.
- Precision.
- Recall.
- Calibration.
- Business lift.
- Loss rate.
- Fairness metrics.

---

## 15. Why Offline AUC Can Look Good but Production Fails

A model can show strong offline AUC but still fail in production because of:

- Leakage.
- Historical selection bias.
- Bad calibration.
- Train/serve skew.
- Delayed or incorrect labels.
- Distribution drift.
- Optimizing approval likelihood instead of incremental conversion or long-term value.
- Measuring ranking quality but not business lift.
- Poor segment-level performance hidden by aggregate metrics.

Interview phrasing:

> High offline AUC does not guarantee production value. I would check whether the model is calibrated, whether the training data reflects the served population, whether labels are mature, whether there is train/serve skew, and whether the objective aligns with actual incremental business value.

---

## 16. Debugging Poor Production Performance

If the model looks strong offline but weak in production, debug in layers.

### Layer 1: Train / Serve Consistency

- Compare feature distributions between training and production.
- Verify feature definitions match.
- Check missing values and default values.
- Confirm online and offline aggregations are equivalent.
- Check feature freshness.

### Layer 2: Label Correctness and Delay

- Validate whether response, approval, risk, or LTV labels have matured.
- Check whether labels are delayed, noisy, or incorrectly joined.
- Separate short-term proxy metrics from long-term realized outcomes.

### Layer 3: Data and Modeling Issues

- Check leakage.
- Check historical selection bias.
- Check calibration drift.
- Check segment-level degradation.
- Check macroeconomic or policy drift.
- Compare against the previous baseline model.

### Layer 4: Operational Decision

- Run shadow evaluation or champion/challenger comparison.
- Roll back if the previous model is safer or materially better.
- Retrain only after the root cause is understood.
- Escalate to risk, compliance, product, or executive leadership if customer harm or regulatory exposure is possible.

Interview phrasing:

> I would break debugging into train/serve consistency, label correctness, and data/model issues. In parallel, I would compare against the previous baseline and use shadow evaluation to quantify the regression before deciding whether to roll back, retrain, or change the objective.

---

## 17. Key Failure Mode and Escalation Path

### Failure Mode

The model learns proxy variables that create disparate impact across protected classes.

### Example

The model may use zip code, education, marketing channel, device type, or other correlated features in a way that systematically excludes certain groups from offers.

### Impact

This could result in:

- Fair lending violations.
- Regulatory scrutiny.
- Customer harm.
- Reputational damage.
- Forced model rollback.
- Audit or external reporting.

### Escalation Path

Escalate beyond engineering to:

- Legal.
- Risk.
- Compliance.
- Model governance.
- Product leadership.
- Executive leadership if customer or regulatory impact is material.

Interview phrasing:

> A key failure mode is the model learning proxy variables that create disparate impact across protected classes. This could systematically exclude certain groups from offers and trigger fair lending, regulatory, and reputational risk. That escalation path must include legal, risk, compliance, model governance, product, and executive leadership.

---

## 18. Key Tradeoff to Defend

I would explicitly trade off short-term model performance for regulatory safety.

### Decision

Restrict or exclude high-risk proxy features until they are fully vetted by legal, risk, compliance, and model governance.

### Cost

- Lower predictive power initially.
- Slower experimentation.
- Potentially lower short-term conversion lift.

### Benefit

- Safer scaling.
- Stronger explainability.
- Lower regulatory risk.
- Lower reputational risk.
- More durable foundation for future model expansion.

Interview phrasing:

> I would trade off short-term model performance for regulatory safety by restricting or excluding high-risk proxy features until they are fully vetted. That may reduce predictive power initially, but it protects the company from regulatory and reputational risk while creating a foundation we can safely expand over time.

---

## 19. Minimal System Sketch

```text
                 +----------------------+
                 | Product Eligibility  |
                 | Credit Policy Rules  |
                 +----------+-----------+
                            |
                            v
+----------------+    +------------+    +------------------+
| Customer Data  |--->| Feature    |--->| Model Scoring    |
| Bureau Data    |    | Platform   |    | Response         |
| Marketing Data |    | Point-in-  |    | Approval         |
| Product Data   |    | Time Safe  |    | Risk             |
| Macro Data     |    +------------+    | Long-Term Value  |
+----------------+                      +--------+---------+
                                                  |
                                                  v
                                      +-----------------------+
                                      | Ranking / Decisioning |
                                      | Eligible Products Only|
                                      +----------+------------+
                                                 |
                                                 v
                                      +-----------------------+
                                      | Channel Activation    |
                                      | Email / App / Web     |
                                      +----------+------------+
                                                 |
                                                 v
                                      +-----------------------+
                                      | Monitoring / Lineage  |
                                      | Drift / Fairness      |
                                      | Calibration / Audit   |
                                      +-----------------------+
```

---

## 20. Final Interview Answer

> I would frame this as a regulated credit-product recommendation system, not an underwriting replacement. The system estimates response probability, approval probability, long-term value, and risk, then ranks eligible products for each customer. Operationally, I would build it as a governed next-best-product platform with shared point-in-time feature definitions, candidate generation, eligibility and compliance filtering, ranking, decisioning, channel activation, and a full feedback loop. Success is measured through PR-AUC, calibration, precision/recall at business thresholds, conversion lift, approval rate, long-term value, loss rate, and fairness metrics.
>
> The key invariants are point-in-time correctness, no leakage, fairness and compliance, lineage and repeatability, and a hard boundary that recommendations cannot override underwriting policy. I would use governed customer, bureau, marketing, product, account, fraud, and macroeconomic data, while excluding post-decision signals and carefully reviewing protected or proxy-sensitive variables.
>
> For models, I would start with interpretable baselines such as logistic regression, then use gradient boosted trees for tabular response, approval, and risk prediction where explainability allows. For product selection, I would use ranking models or product-level scoring. For long-term value, I would use supervised regression, survival modeling, or uplift modeling depending on the business question.
>
> Before launch, I would require time-based validation, out-of-time holdout testing, calibration checks, fairness review, leakage review, model artifact tracking, and shadow comparison against the current baseline. If production performance regresses, I would debug train/serve consistency, label delay, data quality, drift, and objective mismatch before deciding whether to roll back, retrain, or change the optimization target.
>
> The tradeoff I would defend is sacrificing some short-term model performance to avoid high-risk proxy features until legal, risk, compliance, and model governance approve them. In credit, a model that is slightly less predictive but explainable, fair, and governable is often the safer and more scalable choice.
