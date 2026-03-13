# Architecture (v1)

## Flow

Source (arXiv API) -> Ingestion (Python) -> Bronze (raw papers) -> dbt transforms -> Silver/Gold -> API -> Dashboard

## Layers

- **Bronze**: raw, append-only ingestion
- **Silver**: cleaned + standardized entities
- **Gold**: business-ready marts/KPIs

## Operational Controls

- Orchestration: Prefect flow for full pipeline run
- Quality: dbt tests + custom checks in `quality/`
- Runbook: `docs/runbook.md`

## Related Docs

- `docs/system-design.md`
- `docs/data-model.md`
- `docs/devops.md`
- `docs/trend-scoring.md`
- `docs/adr/`
