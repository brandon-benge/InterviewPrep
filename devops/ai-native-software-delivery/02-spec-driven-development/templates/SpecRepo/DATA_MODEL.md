# Data Model Template

> Purpose: Define the system's authoritative entities, relationships, and ownership boundaries
> Goal: Make state, identity, and lifecycle explicit before implementation

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

---

## 5. Schema Evolution

Describe how the model changes safely over time.

- Backward compatibility policy:
- Versioning strategy:
- Migration strategy:
- Rollback strategy:
- Deprecation window:

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

---

## 7. Data Risks

Record known risks or ambiguities in the model.

1. _
2. _
3. _
