# Machine Learning Algorithms — 1 Page Cheat Sheet

## How to Think About It

Start with the problem:

```text
Classification  → predict probability of a class / yes-no outcome
Regression      → predict an expected numeric value
Ranking         → predict a relative score used to order options
Recommendation  → predict what item / offer / content a user is most likely to prefer
Time Series     → predict future value or behavior over time
Anomaly         → predict how unusual something is
```

Important:
- `Classification`, `Regression`, `Ranking`, and `Time Series` are problem types.
- `Logistic Regression`, `Gradient Boosted Trees`, and `Neural Networks` are algorithms.
- That is why classification has multiple algorithms listed: they are different ways to solve the same classification problem.

### Model Types
> A model itself doesn’t have to be tied to a single type. The objective function defines whether it behaves like a classification, regression, or ranking model. In practice, we often use the same algorithm across multiple problem types, and real systems usually combine multiple models to solve different parts of the problem.

- **Classification**
  - Returns: a class probability or label.
  - Used for:
    - fraud detection
    - credit approval
    - click prediction
  - Example input: transaction amount, merchant, time, location, past user behavior
  - Example output: `fraud probability = 0.87` then classify as fraud / not fraud.
  - Binary classification often exposes one probability, while multiclass classification returns one probability per class.
  - Common algorithms:
    - Logistic Regression: learns a weighted combination of features, then maps that score to a probability.
    - Decision Trees: repeatedly split the data on feature thresholds until each leaf predicts a class.
    - Random Forest: trains many decision trees on different samples, then averages their predictions.
    - Gradient Boosted Trees (Extreme Gradient Boosting (XGBoost) / Light Gradient Boosting Machine (LightGBM)) ⭐: builds trees sequentially, where each new tree focuses on correcting the previous trees' errors.
    - Neural Networks: learn multiple layers of nonlinear transformations to map inputs to class probabilities.

- **Regression**
  - Returns: a number.
  - Used for:
    - credit limit
    - risk score
    - expected loss
  - Example input: income, debt, credit history length, payment history
  - Example output: `predicted credit limit = 12000`
  - Common algorithms:
    - Linear Regression: fits a weighted sum of features to predict a numeric value.
    - Ridge / Lasso: linear regression with regularization to reduce overfitting and shrink less useful features.
    - Random Forest Regressor: averages predictions from many regression trees.
    - Gradient Boosting Regressor: builds trees sequentially to reduce numeric prediction error.

- **Ranking**
  - Returns: a score used to order options.
  - Used for:
    - ordering candidate offers
    - search results
    - feed prioritization
  - Example input: user profile plus candidate offers A, B, C
  - Example output: offer A = `0.91`, offer B = `0.62`, offer C = `0.44`
  - Common algorithms:
    - Gradient Boosted Trees (ranking objective, e.g., Extreme Gradient Boosting (XGBoost)): learn scores that place better candidates above worse ones.
    - Neural networks: learn user-item or context-item interactions and output ranking scores.

- **Recommendation**
  - Returns: a preference score for each item, then shows the top items.
  - Used for:
    - which offer to show
    - personalization
    - next-best-action
  - Example input: user watch history, likes, searches, and candidate movies A, B, C
  - Example output: movie A = `0.82`, movie B = `0.31`, movie C = `0.67`
  - Common algorithms:
    - Neural networks: learn complex patterns between users, items, and context.
    - Collaborative filtering: recommends items by finding similar users or similar items from interaction history.
    - Gradient Boosted Trees when recommendation is framed as ranking: score candidate items and return the top ones.

- **Time Series**
  - Returns: a future value, trend, or forecast over time.
  - Used for:
    - transaction patterns
    - behavior over time
    - demand or spend forecasting
  - Example input: monthly spend for the last 12 months
  - Example output: `next month's spend = 2400`
  - Common algorithms:
    - Long Short-Term Memory (LSTM) / Recurrent Neural Network (RNN): process sequences step by step while carrying information forward through time.
    - Transformers: use attention to decide which past time steps matter most for the prediction.

- **Anomaly Detection**
  - Returns: an anomaly score or unusual / not unusual flag.
  - Used for:
    - fraud
    - unusual activity
    - intrusion or outlier detection
  - Example input: transaction amount, merchant, device, location, time, normal account behavior
  - Example output: transaction anomaly score = `0.93`
  - Common algorithms:
    - Isolation Forest: isolates unusual points quickly by randomly splitting the feature space.
    - One-Class Support Vector Machine (SVM): learns the boundary of normal behavior and flags points outside it.
    - Statistical thresholds: mark values as anomalous when they are far from expected ranges or historical patterns.

---

## Common Evaluation Metrics for Classification

- **Class Imbalance**
  - When one class is much rarer than the other, such as fraud vs non-fraud. This matters because a model can look accurate while failing to detect the minority class.

- **Confusion Matrix**
  - A 2x2 table showing prediction outcomes:

  ```text
                   Predicted Positive   Predicted Negative
  Actual Positive      TP                   FN
  Actual Negative      FP                   TN
  ```

- **Accuracy**
  - Overall percent predicted correctly.
  - Formula: `(TP + TN) / (TP + TN + FP + FN)`

- **Precision**
  - Of all predicted positives, how many were actually positive.
  - Formula: `TP / (TP + FP)`

- **Recall**
  - Of all actual positives, how many the model caught.
  - Formula: `TP / (TP + FN)`

- **F1 Score**
  - The harmonic mean of precision and recall. Useful when you want a single metric that balances false positives and false negatives.
  - Formula: `2 * (Precision * Recall) / (Precision + Recall)`

- **ROC**
  - Receiver Operating Characteristic curve. Shows the tradeoff between true positive rate and false positive rate across different classification thresholds.

- **AUC**
  - Area Under the Curve. Usually refers to the area under the ROC curve. Higher is better: `1.0` is perfect, `0.5` is random.

- **PR-AUC**
  - Area under the Precision-Recall curve. Useful when the positive class is rare, such as fraud detection, because it focuses on precision and recall rather than true negatives.

- **Prediction Bias**
  - Whether the model systematically overpredicts or underpredicts positives for the population or for a subgroup. A common simple check is comparing average predicted positive rate to actual positive rate.


- **Calibration**
  - Whether predicted probabilities match real-world outcome rates. For example, among cases scored at `0.80`, about `80%` should actually have the outcome if the model is well calibrated.

- **ROC-AUC**
  - Receiver Operating Characteristic Area Under the Curve. Measures how well the model separates positive and negative classes across all classification thresholds. Useful for understanding overall ranking quality, especially when classes are more balanced.

---

## Common Failure Modes and Data Issues

- **Leakage**
  - The model accidentally uses information that would not truly be available at prediction time, which makes offline performance look unrealistically good. Common examples are using post-decision fields, future events, or labels indirectly embedded in features.

- **Historical Selection Bias**
  - The training data reflects past business decisions rather than the full population. For example, if you only observe repayment outcomes for previously approved applicants, the model learns from a biased sample and may not generalize well to all applicants.

- **Bad Calibration**
  - The ranking may be decent, but the predicted probabilities are not trustworthy. If the model predicts `0.80`, but only `0.55` of those cases actually happen, the model is poorly calibrated and thresholds or risk decisions can become misleading.

- **Train/Serve Skew**
  - The features used in production do not match the features used during training, even if they have the same names. This can happen because of different aggregation logic, missing upstream data, timing differences, or inconsistent preprocessing between offline and online pipelines.

- **Delayed or Incorrect Labels**
  - The true outcome arrives late or is noisy. In lending, fraud, or conversion problems, the final label may take weeks or months to mature, and some labels may be wrong. This can distort training data, slow feedback loops, and make recent model evaluation harder.

- **Distribution Drift**
  - The production data changes over time relative to the training data. Customer behavior, fraud patterns, macro conditions, or marketing channels may shift, causing model performance to degrade even if the model was good at launch.

- **Optimizing Approval Likelihood but Not Incremental Conversion or Long-Term Value**
  - The model learns who is likely to be approved or who already looks easy to convert, rather than who creates additional business value because of the intervention. This can produce a model that looks good on short-term proxy metrics but fails to improve incremental lift, retention, profitability, or customer lifetime value.

- **Business Lift**
  - The real business improvement caused by the model, not just offline model accuracy. Common examples are higher conversion rate, higher approval rate at the same risk level, lower loss rate, higher retention, or better long-term customer value.

What to say:

> I would explicitly check for leakage, biased training data, calibration problems, train/serve skew, label quality issues, and drift. I would also make sure the optimization target matches the real business objective, not just a convenient proxy.

---

## Time-Based Train / Validation / Test / OOT Holdout

When data has a time dimension, split by time instead of random sampling so the model only learns from the past and is evaluated on the future.

Example:

```text
Train           Jan 2023 - Sep 2023
Validation      Oct 2023 - Nov 2023
Test            Dec 2023 - Jan 2024
OOT Holdout     Feb 2024 - Apr 2024
```

- **Train**
  - Fit the model on the oldest window.

- **Validation**
  - Tune hyperparameters, thresholds, and features without touching the final test set.

- **Test**
  - Final pre-launch evaluation on a later time window that the model has never seen.

- **Out-of-Time (OOT) Holdout**
  - A strictly later period kept separate to measure temporal generalization, drift, and whether performance still holds in a new regime.

What to say:

> For temporal data, I use forward-looking splits: train on older data, validate on a later window, test on an even later window, and keep an out-of-time holdout as the most recent unseen period to check robustness against drift.

---

## What Actually Matters (REAL ANSWER)

Priority order:

```text
1. Data quality
2. Feature engineering
3. Algorithm choice
```

---

## Industry Reality (Capital One)

Most common choice:

```text
Gradient Boosted Trees (Extreme Gradient Boosting (XGBoost) / Light Gradient Boosting Machine (LightGBM))
```

Why:
- strong performance on structured data
- handles missing values
- relatively interpretable

---

## When to Choose Which Model

- **Logistic Regression**
  - Choose it when you need a simple, interpretable baseline for binary classification on structured data, especially in regulated settings where explainability matters.

- **Gradient Boosted Trees**
  - Choose them for most tabular prediction problems such as fraud, credit risk, and churn because they usually perform best on structured business data and capture nonlinear relationships well.

- **Recommendation / Ranking Models**
  - Choose them when the goal is to score and order multiple candidates, such as offers, feed items, or search results, rather than predict a single yes/no outcome.

---

## Interview Answer (Memorize This)

> The choice of algorithm depends on the problem type. For most tabular problems like fraud or credit risk, gradient boosted trees are the strongest baseline. For ranking and personalization, we use ranking models or neural networks. In practice, the biggest impact comes from feature engineering and data quality rather than switching algorithms.

---

## Bonus (Standout Point)

> In regulated environments, we also consider interpretability and governance, so simpler models like logistic regression or tree-based models are often preferred unless more complex models provide a clear benefit.
