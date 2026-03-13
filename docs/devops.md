# DevOps Plan

## Hosting
- Frontend/API: Vercel (`data-pipeline-lab-site`)
- Data pipeline code: `data-pipeline-lab`

## Runtime Strategy
- Scheduled refresh job every 6h (initial)
- API serves precomputed/cached data (no direct arXiv calls on request path)

## Environments
- `dev`: local docker + local env vars
- `prod`: Vercel + managed Postgres

## Secrets
- `DATABASE_URL`
- `PIPELINE_CRON_SECRET`
- Optional: `BLOB_READ_WRITE_TOKEN`

## Observability
- Vercel Analytics + Speed Insights
- Pipeline run log table (`pipeline_runs`)
- Basic freshness checks (last successful run)
