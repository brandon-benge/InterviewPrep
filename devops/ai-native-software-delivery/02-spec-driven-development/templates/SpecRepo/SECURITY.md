# Security Template

> Purpose: Define how the system authenticates actors, authorizes actions, and protects data
> Goal: Make trust boundaries and security obligations explicit enough to review and enforce
> Example policy: Any block labeled `Example Only` is illustrative only.

---

## 1. Security Objectives

- Primary assets to protect:
- Primary threats:
- Compliance drivers:
- Abuse scenarios to prevent:

### Example Only

- Primary assets to protect: experiment definitions, tenant boundaries, subject identifiers, admin credentials
- Primary threats: cross-tenant access, unauthorized publish, credential theft, replayed admin requests
- Compliance drivers: internal auditability and region-bound data handling
- Abuse scenarios to prevent: one tenant forcing treatment decisions for another tenant's traffic

---

## 2. Authentication

- Human authentication method:
- Service authentication method:
- Token / credential format:
- Credential rotation policy:

### Example Only

- Human authentication method: corporate SSO via OIDC
- Service authentication method: workload identity plus mTLS
- Token / credential format: JWT with immutable `tenant_id` and service scopes
- Credential rotation policy: automatic rotation every 24 hours for service credentials

---

## 3. Authorization

- Authorization model:
- Tenant isolation model:
- Privileged actions:
- Break-glass policy:

### Example Only

- Authorization model: RBAC with scoped admin roles and service scopes
- Tenant isolation model: every request is authorized against caller identity plus explicit `tenant_id`
- Privileged actions: publish experiment, pause experiment, extend stale-read window
- Break-glass policy: time-bounded elevated role with manager approval and full audit logging

---

## 4. Data Protection

### Data at Rest
- Encryption requirement:
- Key ownership:

### Data in Transit
- Transport protection:
- Internal service requirements:

### Sensitive Data Handling
- PII / secrets / regulated data:
- Masking or redaction rules:
- Retention constraints:

### Example Only

### Data at Rest
- Encryption requirement: KMS-backed encryption for all primary stores and logs
- Key ownership: Platform security team owns key policy

### Data in Transit
- Transport protection: TLS 1.2+
- Internal service requirements: mTLS between runtime, control plane, and event infrastructure

### Sensitive Data Handling
- PII / secrets / regulated data: pseudonymous subject IDs and admin identity metadata
- Masking or redaction rules: never log raw subject IDs or tokens
- Retention constraints: minimize subject-linked data in hot storage and archive per policy

---

## 5. Secrets and Key Management

- Secret storage mechanism:
- Access policy:
- Rotation cadence:
- Audit expectation:

### Example Only

- Secret storage mechanism: centralized secret manager with workload identity access
- Access policy: least privilege per service account
- Rotation cadence: automatic quarterly for long-lived keys, daily for service tokens
- Audit expectation: all secret reads and policy changes are logged

---

## 6. Security Monitoring and Response

- Security logs required:
- Detection signals:
- Incident response owner:
- Containment expectations:

### Example Only

- Security logs required: auth failures, admin role elevation, publish actions, cross-tenant access denials
- Detection signals: unusual tenant access patterns, repeated auth failures, break-glass activation
- Incident response owner: platform security on-call with service owner support
- Containment expectations: revoke affected credentials, isolate impacted tenant or region, preserve evidence

---

## 7. Residual Risks

1. _
2. _
3. _

### Example Only

1. Caller-provided context fields may still carry sensitive data if upstream validation is weak.
2. Tenant-bound JWT claims depend on identity provider correctness.
3. Audit volume during large incidents may create retention cost pressure.
