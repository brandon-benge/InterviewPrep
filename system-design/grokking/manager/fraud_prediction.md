# Fraud Prediction System Design

## 1. Problem Overview

We are predicting, for each attempted card transaction, the probability that the transaction is fraudulent before authorization. The goal is to reduce fraud loss while controlling false declines and keeping the authorization path within 100ms p99.

Success is measured by PR-AUC, recall at a fixed false-positive rate, and calibration error, plus business outcomes like lower confirmed fraud loss rate without materially reducing legitimate approval volume.

Scope starts when an authorization request arrives and ends when the system returns a fraud risk decision or score. The system does not determine final fraud liability, validate fraud labels, permanently block customers by model score alone, or own downstream investigation workflows.

Invariants:
- Latency Invariant: Every in-scope transaction must return a fraud score or policy decision within 100ms p99.
- Auditability Invariant: Every decision must be traceable to the transaction, feature values or feature snapshot reference, model version, policy version, timestamp, and decision reason.
- Human Review Invariant: No customer account is permanently blocked solely because of a model score; durable restrictions require downstream review or explicit policy authority.

---

## 4. Model Overview

We use a logistic regression model to predict the probability of fraud for each transaction:

```text
P(fraud) = 1 / (1 + e^-(w1*x1 + w2*x2 + ... + b))
```

Where:

- `x1, x2, ...` are input features such as amount, location, time, and user behavior patterns.
- `w1, w2, ...` are learned weights for each feature.
- `b` is the bias term.
- `P(fraud)` is the predicted probability that the transaction is fraudulent.

### Training Objective and Imbalance Handling

We train using **weighted binary cross-entropy (log loss)** to handle class imbalance (fraud <1%):

```text
L = - (w1 * y * log(p) + w0 * (1 - y) * log(1 - p))
```

- `w1` (fraud) >> `w0` (non-fraud) to penalize missed fraud more heavily.
- Final decisions are made via **threshold tuning** aligned to business cost (fraud loss vs customer friction), not raw probabilities alone.

### Why Start with Logistic Regression?

Logistic regression is a strong first model because it is:

- Interpretable
- Fast to train
- Fast to serve
- Easier to explain to business, compliance, and risk teams
- Useful as a baseline before moving to more complex models

### Possible Future Model Upgrades

If logistic regression does not provide enough predictive power, the system can evolve toward tree-based models:

- **Random Forest**
  - Uses many decision trees trained independently.
  - Final prediction is based on the aggregate result of many trees.
  - Helps capture non-linear patterns.

- **Gradient Boosting**
  - Builds trees sequentially.
  - Each new tree attempts to correct errors from previous trees.
  - Often performs well on structured tabular data.

---

## 5. Data Features

The model uses **feature-engineered signals expressed as entity + time window + aggregation**. Example high-signal features include:

- `txn_count_last_5min_by_card` (velocity)
- `geo_velocity = distance_km / time_since_last_txn` (impossible travel)
- `is_new_merchant_90d` (merchant novelty)
- `txn_amount / avg_txn_amount_30d` (amount deviation)
- `is_new_device` (device mismatch)

### Feature Categories

#### Transaction Features

Examples:

- Transaction amount
- Merchant category
- Payment method
- Transaction frequency

#### Location Features

Examples:

- Transaction location
- Distance from user's typical location
- Impossible travel patterns
- Country, region, or merchant location risk

#### Time Features

Examples:

- Time of transaction
- Day of week
- Time since previous transaction
- Burst activity over a short time window

#### User Behavior Pattern Features

Examples:

- Average transaction amount for the user
- Typical merchants
- Typical transaction times
- Historical fraud or dispute behavior
- Recent changes in behavior

### Feature Risks

#### Fairness Risk

- Location-based features can act as proxy variables for protected classes.
- Prefer behavioral signals (geo-velocity) over static geo risk.
- Monitor model outcomes across segments to detect bias.

#### Data Leakage Risk

- Features must be computed using only data available at prediction time.
- Example risk: using fraud labels that arrive days later.
- All features must be **time-bounded** to avoid future information leakage.

---

## 6. High-Level System Architecture

The system architecture includes:

- Data ingestion from transaction streams
- Real-time feature extraction
- Model inference service
- Alert generation for suspected fraud

### Architecture Flow

```text
Transaction Stream
        |
        v
Data Ingestion Layer
        |
        v
Real-Time Feature Extraction
        |
        v
Feature Store / Feature Cache
        |
        v
Model Inference Service
        |
        v
Fraud Score + Decision Threshold
        |
        v
Alert Generation / Review Queue / Decision API
```

### Component Responsibilities

#### 1. Data Ingestion Layer

Receives transaction events from upstream payment or transaction systems.

Responsibilities:

- Accept transaction events.
- Validate event schema.
- Preserve transaction identifiers.
- Forward valid events for feature extraction.

#### 2. Real-Time Feature Extraction

Builds features needed for fraud scoring.

Responsibilities:

- Extract transaction amount, location, and time features.
- Compute user behavior pattern features.
- Create rolling aggregates such as recent transaction count or average spend.
- Prepare model-ready feature vectors.

#### 3. Feature Store / Feature Cache

Stores reusable model features.

Responsibilities:

- Serve low-latency features for real-time inference (online store).
- Provide consistent historical features for training (offline store).
- Ensure **training-serving consistency** by using the same feature definitions.
- Store feature computation logic centrally to prevent drift.

### Training vs Serving Consistency

To ensure consistency between offline training and real-time inference:

- Use the same feature definitions for both training and serving.
- Store feature transformations in a centralized feature store.
- Snapshot training data with feature timestamps.
- Validate that real-time features match training distributions.

#### 4. Model Inference Service

Hosts the trained fraud prediction model.

Responsibilities:

- Accept model-ready features.
- Return `P(fraud)` as a probability score.
- Support fast response times for transaction decisioning.
- Log predictions for audit and retraining.

#### 5. Decision Threshold Layer

Converts model probability into an action.

Example:

```text
If P(fraud) >= threshold, flag transaction as suspected fraud.
If P(fraud) < threshold, allow transaction or send to lower-risk path.
```

Responsibilities:

- Apply business-defined threshold.
- Support different thresholds by product, market, or risk tier.
- Balance fraud loss against customer friction.

#### 6. Alert Generation

Generates alerts for suspected fraud.

Responsibilities:

- Create alerts for high-risk transactions.
- Send alerts to review queues or downstream fraud systems.
- Include transaction context and model score.

---

## 7. Evaluation Metrics

We evaluate the model using precision, recall, and F1 score.

### Core Terms

- **True Positive (TP)**: Fraud correctly predicted as fraud.
- **False Positive (FP)**: Legitimate transaction incorrectly predicted as fraud.
- **False Negative (FN)**: Fraud incorrectly predicted as legitimate.
- **True Negative (TN)**: Legitimate transaction correctly predicted as legitimate.

### Precision

Precision answers:

> When the model predicts fraud, how often is it correct?

```text
Precision = TP / (TP + FP)
```

High precision means fewer legitimate customers are incorrectly flagged.

### Recall

Recall answers:

> How much actual fraud did the model catch?

```text
Recall = TP / (TP + FN)
```

High recall means fewer fraudulent transactions are missed.

### F1 Score

F1 score balances precision and recall.

```text
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

F1 is useful when both false positives and false negatives matter.

### Additional Metrics to Consider

#### PR-AUC

PR-AUC means Precision-Recall Area Under the Curve.

It is useful for fraud because fraud datasets are usually imbalanced, meaning fraud is much rarer than legitimate activity.

#### ROC-AUC

ROC-AUC means Receiver Operating Characteristic Area Under the Curve.

It measures how well the model separates fraud from non-fraud across many thresholds.

However, for highly imbalanced fraud problems, PR-AUC is often more useful than ROC-AUC.

---

## 8. Class Imbalance Handling

Fraud is usually rare, so the model may learn to predict "not fraud" too often.

Approaches:

### Resampling

- **Oversampling**: Duplicate or synthesize fraud examples.
- **Undersampling**: Remove some legitimate examples.

### Class Weighting

Class weighting assigns a higher penalty when the model misses fraud.

Example:

```text
Missing fraud may be treated as 10x more costly than a false alarm.
```

This helps the model pay more attention to rare fraud cases.

---

## 9. Threshold Tuning

The model outputs a probability, not a final business decision.

Example:

```text
P(fraud) = 0.73
```

A threshold determines what action to take.

Example:

```text
If threshold = 0.70, then 0.73 is flagged as suspected fraud.
If threshold = 0.90, then 0.73 is not flagged.
```

### Threshold Tradeoff

- Lower threshold:
  - Catches more fraud.
  - Increases recall.
  - Creates more false positives.
  - Adds customer friction.

- Higher threshold:
  - Reduces false positives.
  - Improves customer experience.
  - May miss more fraud.
  - Lowers recall.

### Advanced Decision Policy

- Use **segment-based thresholds** (e.g., new users vs long-tenured users).
- Introduce a **review band**:
  - Approve (low risk)
  - Review (medium risk)
  - Decline (high risk)
- Optimize thresholds based on **expected business cost**, not just accuracy.

---

## 10. Correctness Invariants

### Invariant 1: Every Scored Transaction Has a Traceable Model Decision

For every transaction scored by the fraud system, the system must persist the transaction ID, feature version, model version, fraud score, threshold, and final decision.

Reason:

- Supports auditability.
- Enables debugging.
- Enables model performance review.

### Invariant 2: Model Decisions Must Be Reproducible for Audit

For any historical fraud decision, the system must be able to explain which model version, feature values, and threshold produced the decision.

Reason:

- Needed for compliance and customer disputes.
- Prevents silent model behavior changes from becoming untraceable.

### Invariant 3: Missing Critical Features Must Not Silently Produce a Normal Decision

If required features are missing or stale, the system must either use a defined fallback path or route the transaction to review.

Reason:

- Prevents false confidence.
- Makes degraded behavior explicit.

---

## 11. Failure Modes and Escalation Paths

### Failure Mode 1: Feature Store Is Unavailable

Impact:

- Model may not have user behavior pattern features.

Possible response:

- Use a reduced feature model.
- Fall back to rules.
- Route high-risk transactions to manual review.

### Failure Mode 2: Model Inference Service Is Slow or Down

Impact:

- Transaction decisioning latency increases.

Possible response:

- Use cached risk scores where safe.
- Apply deterministic rules for known high-risk patterns.
- Fail open or fail closed depending on business and regulatory requirements.

### Failure Mode 3: Fraud Pattern Changes Over Time

Impact:

- Model quality degrades.
- Recall may drop as fraudsters adapt.

Possible response:

- Monitor precision, recall, false positives, and false negatives.
- Retrain model using confirmed fraud labels.
- Review threshold settings.

### Failure Mode 4: Feature Drift or Distribution Shift

Impact:

- Model performance degrades over time.
- False positives or false negatives increase.

Possible response:

- Monitor feature distributions and model outputs.
- Gate or clip unstable features (e.g., anomaly scores).
- Recalibrate probabilities or retrain model after validation.

---

## 12. Operational Monitoring

Monitor:

- Transaction scoring latency
- Model inference error rate
- Feature freshness
- Feature missing rate
- Alert volume
- Precision
- Recall
- F1 score
- PR-AUC
- Fraud loss rate
- False positive rate
- Calibration error
- Feature drift metrics
- Segment-level performance (e.g., by geography, tenure)

---

## 13. Director-Level Tradeoffs

| Decision | Tradeoff |
|---|---|
| Logistic regression vs gradient boosting | Interpretability vs predictive power |
| Lower threshold vs higher threshold | More fraud caught vs more customer friction |
| Real-time features vs batch features | Freshness vs system complexity |
| Fail open vs fail closed | Customer experience vs fraud risk |
| Manual review vs automated blocking | Operational cost vs faster fraud prevention |
| Anomaly detection usage | Novel pattern detection vs calibration and precision control |

---

## 14. Interview Summary Answer

I would frame fraud prediction as a supervised classification problem where we predict the probability that a transaction is fraudulent in real time. I would start with logistic regression as a baseline due to interpretability and speed, then evolve toward gradient boosted trees to capture nonlinear interactions.

The system would ingest transaction streams, compute real-time and historical features via a feature store, and serve low-latency predictions. A decision layer would apply calibrated, segment-aware thresholds and introduce a review band to balance fraud loss against customer friction.

Key risks include class imbalance, feature drift, data leakage, and fairness. These are mitigated through weighted loss functions, strict time-based feature computation, monitoring, and auditability. Success is measured using PR-AUC, recall at fixed false-positive rates, calibration, and business metrics like fraud loss and false declines.
