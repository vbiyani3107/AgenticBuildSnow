# Session: Daily scheduled job to list top 10 incidents (read-only)

| Field | Value |
|-------|-------|
| **Session ID** | `20260617-090539-daily-incident-list-job` |
| **Jira** | SN-DO-SCHED-JOB |
| **Module** | incident-management |
| **Status** | completed |
| **Current phase** | done |
| **Instance** | accenture-demo |
| **Active** | false |

## Requirement

Create a global scheduled job to run daily at 3 PM and list 10 incidents (read-only).

## Delivered on instance

| Artifact | sys_id |
|----------|--------|
| Scheduled Script `[SN-DO] Daily Top 10 Incidents List` | 989d7d112b29c39015a9f5685e91bf91 |
| Update Set `[20260617-090539-daily-incident-list-job] Daily Incident List Job` | ed8db115fb294790a5c9ff8165efdcbf |

## Phase artifacts

| Phase | Status | Key file |
|-------|--------|----------|
| Analyze | completed | analyze/handoff.md |
| Build | completed | build/implementation-log.md |
| Test | completed (PARTIAL) | test/test-report.md |
| Document | completed | document/jira-story.md |

## Pipeline

See [pipeline-execution-report.md](pipeline-execution-report.md)
