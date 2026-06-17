# [SN-DO-SCHED-JOB] Daily scheduled job to list top 10 incidents (read-only)

**Session ID**: `20260617-090539-daily-incident-list-job`  
**Session folder**: `.cursor/servicenow-sessions/20260617-090539-daily-incident-list-job/`

| Field | Value |
|-------|-------|
| Module | Incident Management |
| Instance tested | accenture-demo |
| Update Set | [20260617-090539-daily-incident-list-job] Daily Incident List Job (`ed8db115fb294790a5c9ff8165efdcbf`) |
| Status | Partial — functional complete; US capture manual step |

---

## Summary

A global scheduled script job was created on accenture-demo to run **daily at 3:00 PM** (instance local time). Each run queries the **10 most recently created incidents** and logs them via `gs.info` in a **strictly read-only** manner. The job is active and verified on the dev instance. Update Set packaging via MCP REST did not auto-capture the component — a one-time UI save is required before migration.

## Original Requirement

Create a global scheduled job to run daily at 3 PM and list 10 incidents (read-only). Run full pipeline — build, test, and document.

## Autonomous decisions applied

| Decision | Value | Source |
|----------|-------|--------|
| Job name | `[SN-DO] Daily Top 10 Incidents List` | DEFAULT |
| Incident selection | Newest 10 by sys_created_on DESC | DEFAULT |
| Output | gs.info log lines | DEFAULT |
| Time zone | Instance default (empty) | DEFAULT |
| Update Set name | `[20260617-090539-daily-incident-list-job] Daily Incident List Job` | DEFAULT |
| Scope | Global | USER + DEFAULT |

## Design decisions

- Used `sysauto_script` (Scheduled Script) rather than Flow — matches explicit scheduled job request
- `run_type=daily`, `run_time=1970-01-01 15:00:00` for 3 PM daily
- No state filter — lists any incident state
- Script avoids all DML (`update`, `insert`, `deleteRecord`)

**Out of scope**:
- Production deployment
- Email/notification delivery
- Incident record modifications

## Solution Overview

```
Daily 3 PM (instance TZ)
        │
        ▼
[SN-DO] Daily Top 10 Incidents List (sysauto_script)
        │
        ▼
GlideRecord('incident') — orderByDesc sys_created_on, limit 10
        │
        ▼
gs.info per incident (number, state, short_description)
```

### Artifacts Changed

| Type | Name | sys_id | Purpose |
|------|------|--------|---------|
| Update Set | [20260617-090539-daily-incident-list-job] Daily Incident List Job | ed8db115fb294790a5c9ff8165efdcbf | Migration packaging |
| Scheduled Script | [SN-DO] Daily Top 10 Incidents List | 989d7d112b29c39015a9f5685e91bf91 | Daily read-only incident listing |

### Configuration Details

**Schedule**: daily at 15:00:00 (3 PM)  
**Script** (read-only):

```javascript
var LOG_PREFIX = '[SN-DO] Daily Top 10 Incidents List: ';
var gr = new GlideRecord('incident');
gr.orderByDesc('sys_created_on');
gr.setLimit(10);
gr.query();
var count = 0;
while (gr.next()) {
    count++;
    gs.info(LOG_PREFIX + count + ' | ' + gr.number + ' | ' + gr.getDisplayValue('state') + ' | ' + gr.short_description);
}
gs.info(LOG_PREFIX + 'Listed ' + count + ' incident(s).');
```

## Implementation Notes

- Update Set created and set current via GlideUpdateSet background script
- Scheduled job created via SN-Create-Record
- **Known limitation**: Update Set shows 0 components after MCP create — manual UI save needed to capture sysauto_script for migration

## Testing Summary

| AC# | Result |
|-----|--------|
| AC1 — Job schedule | PASS |
| AC2 — Read-only execution | PASS |
| AC3 — No duplicate | PASS |
| AC4 — Update Set component | BLOCKED (manual UI) |

**Overall test result**: PARTIAL (3 PASS, 1 BLOCKED)

Functional behavior verified with MCP queries and before/after incident timestamp comparison. High confidence in job correctness on dev instance.

## Deployment Instructions

1. On accenture-demo, set current Update Set: `[20260617-090539-daily-incident-list-job] Daily Incident List Job`
2. Open **System Definition → Scheduled Jobs** → `[SN-DO] Daily Top 10 Incidents List` → **Update** (capture in US)
3. Complete Update Set
4. Migrate to test → verify schedule shows Daily 3:00 PM
5. Optional smoke: **Execute Now** → check **System Logs** for `[SN-DO] Daily Top 10 Incidents List:` entries
6. Prod: human approval required

## Rollback

| Artifact | Action |
|----------|--------|
| Scheduled Script | Set `active=false` or delete sys_id `989d7d112b29c39015a9f5685e91bf91` |
| Update Set | Revert / do not migrate |

## Support & Troubleshooting

| Symptom | Likely cause | Check |
|---------|--------------|-------|
| No log output at 3 PM | Timezone / job inactive | Scheduled Jobs → active, run_time, instance TZ |
| Empty list in logs | Fewer than 10 incidents exist | Incident list; script logs count |
| Job not in Update Set | REST create without capture | UI save with US current |

## References

- Session manifest: `.cursor/servicenow-sessions/20260617-090539-daily-incident-list-job/SESSION.md`
- Handoff: `analyze/handoff.md`
- Implementation log: `build/implementation-log.md`
- Test report: `test/test-report.md`

---

## Jira Description (copy-paste)

**Summary**: Global scheduled job lists top 10 incidents daily at 3 PM (read-only).

**What was built**:
- Scheduled Script `[SN-DO] Daily Top 10 Incidents List` (sysauto_script)
- Runs daily at 15:00 instance time
- Logs 10 newest incidents to system log — no record changes

**Instance**: accenture-demo (dev)  
**Update Set**: [20260617-090539-daily-incident-list-job] Daily Incident List Job  
**Job sys_id**: 989d7d112b29c39015a9f5685e91bf91

**Testing**: Schedule verified PASS; read-only verified PASS; US capture needs manual UI save before migrate.

**Rollback**: Deactivate scheduled job.

---

*Generated by Documentation Agent — 2026-06-17*
