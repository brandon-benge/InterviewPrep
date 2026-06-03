# Canonical Service Catalog

## Purpose

The canonical service catalog is the authoritative map of business capabilities, repositories, runtime components, owners, interfaces, and dependency relationships across a software estate.

It is most important when the organization has many repositories or services and needs a dependable way to answer:

- Which business capability does this repo support?
- Which runtime components does this repo produce?
- Who owns the component?
- What APIs, events, jobs, data products, or infrastructure does it provide?
- What upstream dependencies does it require?
- What downstream systems consume it?
- Which dependency edges are declared, observed, stale, or unverified?

## Industry Position

The service catalog itself is an established industry pattern. Tools such as Backstage and commercial developer portals commonly model components, ownership, APIs, systems, dependencies, and scorecards. The common pattern is to maintain catalog data from repo-local descriptors, service ownership metadata, API contracts, platform metadata, and developer portal workflows.

Using artificial intelligence to infer or propose catalog updates is an emerging extension, not a settled industry standard. When used, it should produce evidence-backed update proposals, not silently mutate the canonical catalog.

## Canonical Mapping Fields

| Field | Meaning |
|---|---|
| Business capability | Customer, product, or business function supported by the component |
| Domain | Bounded context, platform area, or organizational domain |
| Repository | Source repository containing implementation and local specs |
| Runtime component | Service, worker, job, library, application, pipeline, or data product |
| Owning team | Team accountable for correctness, operation, and lifecycle |
| Provided interfaces | APIs, events, packages, data products, or infrastructure outputs exposed by the component |
| Consumed interfaces | APIs, events, packages, data products, or infrastructure inputs required by the component |
| Upstream dependencies | Components this component depends on |
| Downstream consumers | Components that depend on this component |
| Criticality | Tier, blast radius, compliance sensitivity, or production importance |
| Evidence source | Contract, repo manifest, deployment metadata, telemetry, trace, code scan, or owner assertion |
| Verification state | Declared, observed, reconciled, stale, disputed, or unknown |

## Catalog Update Flow

The catalog should maintain the declared component map.

Catalog updates commonly come from:

- repo-local component manifests
- `SpecRepo` architecture and data model files
- OpenAPI, AsyncAPI, GraphQL, package, and event contracts
- deployment metadata such as Kubernetes labels, Terraform outputs, or service mesh configuration
- ownership and team metadata

Build and release pipelines can validate or publish this metadata, but they are not the only maintenance path. Developer portals, catalog ingestion jobs, repository scanners, and platform automation may also update the catalog.

The update flow can produce a catalog diff:

| Change Type | Example |
|---|---|
| New component | A new worker is introduced |
| Removed component | A deprecated job is deleted |
| New dependency edge | Service A now calls Service B |
| Removed dependency edge | A legacy database dependency is removed |
| Interface change | An API contract adds a required field |
| Ownership change | Component ownership moves to another team |
| Criticality change | A service becomes tier 1 |

High-risk catalog changes should be reviewed before release promotion.

## Runtime Drift Signals

Runtime evidence can help detect catalog drift, but this is not yet a universal industry-standard catalog maintenance flow.

Observability systems may compare the canonical catalog against runtime evidence such as:

- OpenTelemetry traces
- service mesh traffic
- API gateway logs
- deployment events
- incident records
- event broker metadata
- database access telemetry

When runtime behavior disagrees with the catalog, the system may raise a catalog drift finding for review.

Examples:

| Catalog Claim | Runtime Evidence | Finding |
|---|---|---|
| `checkout-api` depends on `payment-api` | Traces also show calls to `risk-api` | Undeclared dependency |
| `orders-worker` no longer consumes `OrderCreated` | Broker metadata shows active consumption | Stale catalog removal |
| `identity-api` is tier 2 | Incident impact shows tier 1 blast radius | Criticality mismatch |

## AI Role

Artificial intelligence may:

- infer dependency edges from code, contracts, deployment metadata, and telemetry
- summarize catalog drift
- propose catalog updates
- identify missing owners or ambiguous component boundaries
- generate dependency-aware review and release risks

Artificial intelligence should not silently change authoritative ownership, criticality, or high-impact dependency mappings. Material changes require human approval from the accountable owner, tech lead, or platform governance process.

For an industry-standard framing, AI-assisted catalog maintenance should be treated as optional augmentation around the service catalog, not as the core catalog source of truth.

## Relationship To SpecRepo

Repo-local `SpecRepo` files describe local system intent and constraints.

The canonical service catalog describes cross-repo truth.

The two should stay aligned:

- `ARCHITECTURE.md` should describe the component's intended dependencies.
- `DATA_MODEL.md` should describe owned and consumed data.
- `API_CONTRACTS.yaml` should describe provided and consumed interfaces.
- Release artifacts should publish declared component metadata.
- Runtime evaluation may detect observed dependency drift and raise review findings.

For large estates, the service catalog becomes the dependency source of truth, while each repo remains the source of truth for local design intent.
