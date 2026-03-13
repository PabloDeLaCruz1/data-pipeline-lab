# ADR 001: Storage Choice

## Status
Accepted

## Context
We need persistent, queryable history for trend charts and metrics while keeping ops simple on Vercel.

## Decision
Adopt Postgres as primary storage for structured analytics tables.
Use object storage (Blob/S3) optionally for raw snapshots/artifacts.

## Consequences
- Enables fast historical queries and chart APIs
- Avoids direct external API dependence in request path
- Adds DB management responsibility
