# Data Model Template

> Purpose: Define the system's authoritative entities, relationships, and ownership boundaries
> Goal: Make state, identity, and lifecycle explicit before implementation
> Example policy: Any block labeled `Example Only` is illustrative only.

---

## 1. Entities

List each core domain object and why it exists.

### Entity: _[name]_
- Purpose:
- Authoritative source:
- Mutable or immutable:
- Sensitive fields:
- Retention expectation:

### Entity: _[name]_
- Purpose:
- Authoritative source:
- Mutable or immutable:
- Sensitive fields:
- Retention expectation:

### Example Only

### Entity: `Experiment`
- Purpose: Defines targeting rules and available variants
- Authoritative source: Control-plane metadata store
- Mutable or immutable: Mutable by versioned publish only
- Sensitive fields: Tenant ID, rollout policy, targeting predicates
- Retention expectation: Retain all published versions for audit

### Entity: `AssignmentRecord`
- Purpose: Records the decision served for a subject and experiment version
- Authoritative source: Assignment service write path
- Mutable or immutable: Immutable once written
- Sensitive fields: Subject ID hash, tenant ID
- Retention expectation: 90 days hot, 1 year archived

---

## 2. Relationships

Describe how entities connect and any cardinality constraints.

### Relationship: _[Entity A] -> [Entity B]_
- Cardinality:
- Ownership direction:
- Delete behavior:
- Consistency expectation:

### Relationship: _[Entity A] -> [Entity C]_
- Cardinality:
- Ownership direction:
- Delete behavior:
- Consistency expectation:

### Example Only

### Relationship: `Experiment -> Variant`
- Cardinality: One-to-many
- Ownership direction: Experiment owns variants
- Delete behavior: Variants may not survive experiment deletion
- Consistency expectation: Strong consistency within a published version

### Relationship: `Experiment -> AssignmentRecord`
- Cardinality: One-to-many
- Ownership direction: AssignmentRecord references but does not own Experiment
- Delete behavior: Assignment history is retained even if experiment is retired
- Consistency expectation: Assignment must reference a valid published experiment version

---

## 3. Keys

Define identity and lookup strategy.

### Primary Keys
- _[entity]_:

### Foreign Keys
- _[entity.field -> other_entity.id]_:

### Natural Keys
- _[if any]_:

### Idempotency / Dedup Keys
- _[request or event keying strategy]_:

### Partition / Shard Keys
- _[if relevant]_:

### Example Only

### Primary Keys
- `experiment`: `experiment_id`
- `assignment_record`: `assignment_id`

### Foreign Keys
- `assignment_record.experiment_version_id -> experiment_version.id`

### Natural Keys
- `tenant_id + experiment_key`

### Idempotency / Dedup Keys
- `tenant_id + experiment_version_id + subject_id + request_id`

### Partition / Shard Keys
- `tenant_id` first, then hash of `subject_id`

---

## 4. Lifecycle

Define valid states and transitions.

### Entity: _[name]_
- States:
- Creation path:
- Update path:
- Terminal states:
- Invalid transitions:

### Entity: _[name]_
- States:
- Creation path:
- Update path:
- Terminal states:
- Invalid transitions:

### Example Only

### Entity: `Experiment`
- States: draft, validated, active, paused, archived
- Creation path: Created by growth engineer as draft
- Update path: Draft changes produce a new version candidate; activation publishes immutable version
- Terminal states: archived
- Invalid transitions: archived -> active without explicit restore workflow

### Entity: `AssignmentRecord`
- States: emitted, delivered, reconciled
- Creation path: Created during assignment evaluation
- Update path: Delivery/reconciliation metadata may be appended
- Terminal states: reconciled
- Invalid transitions: assignment payload mutation after emit

---

## 5. Schema Evolution

Describe how the model changes safely over time.

- Backward compatibility policy:
- Versioning strategy:
- Migration strategy:
- Rollback strategy:
- Deprecation window:

### Example Only

- Backward compatibility policy: Assignment API remains backward compatible for one minor version window
- Versioning strategy: Immutable experiment versions plus versioned event schemas
- Migration strategy: Additive schema changes first, backfill, then reader migration
- Rollback strategy: Re-point active config to prior experiment version
- Deprecation window: 90 days for old API fields

---

## 6. Ownership

Define which system owns which data and who may mutate it.

### System Ownership
- _[entity or field]_ is owned by _[service/system/team]_.

### Write Authority
- _[actor/service]_ may create:
- _[actor/service]_ may update:
- _[actor/service]_ may delete:

### Derived vs Authoritative Data
- Authoritative records:
- Derived / cached / replicated records:

### Example Only

### System Ownership
- `Experiment` is owned by the experiment control plane team
- `AssignmentRecord` is owned by the assignment runtime service

### Write Authority
- Growth engineer may create: draft experiments
- Publish service may update: experiment activation state
- No actor may delete: immutable audit or assignment history directly

### Derived vs Authoritative Data
- Authoritative records: experiment definitions, published versions, assignment records
- Derived / cached / replicated records: regional config caches, analytics aggregates

---

## 7. Data Risks

Record known risks or ambiguities in the model.

1. _
2. _
3. _

### Example Only

1. Subject identity normalization may differ across caller services.
2. Some tenants may require longer retention for exposure history.
3. Assignment replay semantics during reprocessing need explicit policy.
