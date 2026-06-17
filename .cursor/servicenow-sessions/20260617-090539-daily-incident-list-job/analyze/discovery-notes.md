# Discovery Notes — 20260617-090539-daily-incident-list-job

**Date**: 2026-06-17  
**Instance**: accenture-demo (`https://accentureservicessrodemo4.service-now.com`)

## Instance

| Field | Value |
|-------|-------|
| Name | accenture-demo |
| Auth | basic |
| Scope for job | Global |

## Artifact table: sysauto_script

Scheduled Script Execution table supports:
- `name`, `active`, `run_type`, `run_time`, `run_dayofweek`, `run_dayofmonth`, `time_zone`
- `script` (script_plain, max 8000 chars)
- `conditional`, `condition`
- `sys_scope` — global for this requirement

### Sample daily job pattern (from instance)

Existing jobs use `run_type: periodically` for interval-based runs. For fixed daily time, use `run_type: daily` with `run_time` set to 15:00:00 (3 PM instance local time).

Example `run_time` format on instance: `1970-01-01 08:00:00` (epoch date + time component).

## Duplicate check

Query: `nameLIKE[SN-DO]` on `sysauto_script` → **0 records** (no prior SN-DO scheduled jobs).

## Incident table

Target table: `incident` — standard ITSM table. Read-only query via `GlideRecord` with `setLimit(10)` and `orderByDesc('sys_created_on')` is appropriate.

## Update Set

No dedicated in-progress global Update Set for this session yet. Will create new Update Set per default-decisions.md.
