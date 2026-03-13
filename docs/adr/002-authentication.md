# ADR 002: Authentication Strategy

## Status
Accepted

## Context
Scheduled jobs and refresh endpoints need protection without introducing full user auth in v1.

## Decision
Use shared secret token auth for internal cron/refresh endpoints (`PIPELINE_CRON_SECRET`).
No end-user authentication in v1.

## Consequences
- Simple and fast to implement
- Sufficient for internal project operations
- Must rotate secrets and avoid exposing endpoints publicly
