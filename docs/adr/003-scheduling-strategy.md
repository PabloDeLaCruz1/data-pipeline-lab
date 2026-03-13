# ADR 003: Scheduling Strategy

## Status
Accepted

## Context
Trend data should refresh regularly without manual runs.

## Decision
Use scheduled runs every 6 hours (initial), via platform cron calling refresh workflow.
Revisit cadence once usage and cost patterns are observed.

## Consequences
- Keeps data fresh enough for daily/weekly trend usage
- Controls cost vs always-on processing
- Requires run monitoring and retry handling
