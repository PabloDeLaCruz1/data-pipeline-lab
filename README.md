# data-pipeline-lab

An end-to-end data engineering project by Clanker + Pablo.

## Goal
Build a production-style analytics pipeline:

1. **Ingest** source data (API/files)
2. **Land** raw data (Bronze)
3. **Transform** to clean/business models (Silver/Gold)
4. **Validate** with data quality checks
5. **Orchestrate** end-to-end runs
6. **Serve** analytics/dashboard outputs

## Project Structure

- `ingestion/` — extract/load scripts
- `warehouse/` — schema and SQL bootstrap
- `transforms/dbt/` — dbt models/tests/docs
- `quality/` — custom validation checks
- `orchestration/` — workflow definitions
- `dashboards/` — BI assets and metric specs
- `docs/` — architecture, runbook, decisions
- `scripts/` — local utility scripts
- `tests/` — pipeline tests

## Initial Stack (v1)

- Python 3.11+
- PostgreSQL (local via Docker)
- dbt-core + dbt-postgres
- Prefect (orchestration)

## Quick Start (scaffold)

```bash
cd data-pipeline-lab
docker compose up -d
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Next Milestones

- [ ] Define domain + source dataset
- [ ] Build first ingestion job
- [ ] Create Bronze/Silver/Gold models in dbt
- [ ] Add quality checks + orchestration flow
- [ ] Publish dashboard + demo runbook
