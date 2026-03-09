# BI Tools and Data Modeling

Business Intelligence (BI) tools help teams explore data, build dashboards, and make decisions using trusted metrics from warehouse or lakehouse systems.

## BI Tool Categories
| Category | Purpose | Common Examples |
|---|---|---|
| Dashboarding / Self-Service BI | Build reports, dashboards, and ad-hoc analysis | Tableau, Power BI, Looker, Sigma |
| Semantic / Metrics Layer | Centralize business metric definitions and governance | LookML (Looker), dbt Semantic Layer, Cube |
| Embedded Analytics | Show analytics inside customer-facing products | Apache Superset (custom embedding), Metabase, ThoughtSpot Embedded |
| Data Apps / Notebook BI | Interactive exploration and lightweight app-style analytics | Hex, Mode, Observable |

## Common BI Capabilities
- Dashboard creation and sharing
- Ad-hoc SQL and drill-down analysis
- Scheduled reports and alerting
- Role-based access control
- Row/column-level security
- Cached query results and extracts
- Metadata catalog/search for discoverability
- Data lineage and usage monitoring

## Key Definitions
- `Fact table`: Stores measurable business events (for example: order amount, click count, session duration) at a defined grain.
- `Dimension table`: Stores descriptive attributes used to slice facts (for example: customer, product, date, geography).
- `Grain`: The level of detail represented by one row in a fact table.
- `Star schema`: One central fact table connected to multiple dimensions.
- `Slowly Changing Dimension (SCD)`: Technique for tracking historical changes in dimension attributes.
- `Semantic layer`: Central place where business metrics and definitions are modeled once and reused everywhere.

## Best Practices for Data Design
- Define table grain before writing transformations.
- Keep raw, curated, and serving layers separate.
- Use conformed dimensions across domains (same `customer_id` meaning everywhere).
- Prefer additive/semi-additive metrics that aggregate correctly.
- Model time explicitly (`event_time`, `ingestion_time`, timezone policy).
- Version and document metric definitions.
- Design partitioning/clustering for top BI filters.
- Pre-aggregate expensive queries when dashboard latency matters.

## Key Things To Get Right
- Metric consistency: one definition of core KPIs across all dashboards.
- Data quality checks: freshness, uniqueness, null rates, and reconciliation against sources.
- Access control: enforce PII masking and least privilege policies.
- Performance: fix small files, optimize joins, and tune hot queries.
- Cost controls: monitor expensive dashboards and constrain runaway queries.
- Ownership: clear owners for pipelines, semantic models, and dashboards.
- SLA communication: publish data freshness and incident status for BI consumers.

## Interview Q&A
- Q: How do you avoid metric drift across BI dashboards?
	A: Define KPIs once in a semantic layer, version the logic, and prohibit ad-hoc redefinitions in individual dashboards.
- Q: When should you use a semantic layer instead of dashboard-level calculations?
	A: Use a semantic layer whenever a metric is shared across teams or reused in many reports to ensure consistency and governance.
- Q: How do you design fact and dimension tables for both flexibility and performance?
	A: Set a clear fact grain, use conformed dimensions, and optimize partitioning/clustering for the highest-frequency BI filters.
- Q: What are common causes of slow BI dashboards, and how do you fix them?
	A: Slow dashboards usually come from poor model design and expensive joins, fixed by pre-aggregations, query tuning, and storage/layout optimization.

## See Also
- [Big Data Storage Platforms](./big-data-storage-platforms.md)
- [Data Pipelines](./data-pipelines.md)
- [Batch Processing](./batch-processing.md)
- [Stream Processing](./stream-processing.md)
