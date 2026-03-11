# Architecture (v1)

## Flow

Source (API/CSV) -> Ingestion (Python) -> Bronze (raw tables) -> dbt transforms -> Silver/Gold -> Dashboard

## Layers

- **Bronze**: raw, append-only ingestion
- **Silver**: cleaned + standardized entities
- **Gold**: business-ready marts/KPIs

## Operational Controls

- Orchestration: Prefect flow for full pipeline run
- Quality: dbt tests + custom checks in `quality/`
- Runbook: `docs/runbook.md` (next)
