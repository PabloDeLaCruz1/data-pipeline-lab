# Runbook (v1)

## Start infra

```bash
docker compose up -d
```

## Run ingestion

```bash
python ingestion/load_sample.py
```

## Run orchestrated flow

```bash
python orchestration/flow.py
```
