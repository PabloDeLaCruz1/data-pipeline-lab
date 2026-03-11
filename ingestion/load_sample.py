"""Sample ingestion scaffold: CSV -> Postgres bronze table."""

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import os


def main():
    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "5433")
    db = os.getenv("PG_DB", "analytics")
    user = os.getenv("PG_USER", "pipeline")
    pwd = os.getenv("PG_PASSWORD", "pipeline")

    engine = create_engine(f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}")

    sample = Path(__file__).parent / "sample_data.csv"
    if not sample.exists():
      pd.DataFrame([
        {"record_id": 1, "category": "demo", "amount": 100.0},
        {"record_id": 2, "category": "demo", "amount": 250.0},
      ]).to_csv(sample, index=False)

    df = pd.read_csv(sample)
    df.to_sql("bronze_sample_events", engine, schema="public", if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into public.bronze_sample_events")


if __name__ == "__main__":
    main()
