# Data Model (v1)

## papers
- `paper_id` (PK)
- `published_at`
- `title`
- `abstract`
- `categories`
- `ingested_at`

## keyword_daily
- `date`
- `keyword`
- `theme`
- `count`
- `share`

## trend_daily
- `date`
- `keyword`
- `theme`
- `count_7d`
- `count_prev_7d`
- `share_7d`
- `share_prev_7d`
- `score`

## pipeline_runs
- `run_id` (PK)
- `started_at`
- `finished_at`
- `status`
- `rows_upserted`
- `notes`
