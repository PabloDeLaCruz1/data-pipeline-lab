# System Design

## Objective
Build a production-style research signal pipeline that ingests arXiv metadata, computes trend acceleration metrics, and serves dashboard-ready outputs.

## Components

1. Ingestion job (scheduled)
2. Storage layer (Postgres-first)
3. Transformation layer (dbt)
4. API serving layer (Next.js API routes)
5. Web visualization layer (data-pipeline-lab-site)

## Data Flow

arXiv -> Bronze (`papers`) -> Silver (normalized text/date) -> Gold (`keyword_daily`, `trend_daily`) -> API -> UI charts/tables

## Non-Goals (v1)

- Multi-tenant auth
- Real-time streaming ingestion
- Heavy MLOps workflows
