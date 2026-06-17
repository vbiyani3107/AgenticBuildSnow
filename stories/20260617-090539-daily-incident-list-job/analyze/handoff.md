# Handoff Document

**Session ID**: 20260617-090539-daily-incident-list-job  
**Session folder**: `stories/20260617-090539-daily-incident-list-job/`  
**Story ID**: SN-DO-SCHED-JOB  
**Title**: Daily scheduled job to list top 10 incidents (read-only)  
**Module**: incident-management  
**SDLC phase at handoff**: Design complete → ready for Build  
**Author (Analysis Agent)**: 2026-06-17  
**Target Instance**: accenture-demo  
**Handoff mode**: READY FOR DEVELOPMENT  
**Autonomous decisions**: 8 defaults applied — see §3

---

## 1. Requirement Summary

Create a **global** scheduled script job that runs **daily at 3:00 PM** (instance local time). The job must query the **incident** table and **list 10 incidents** in a read-only manner (no inserts, updates, or deletes). Output is logged via `gs.info` for operational visibility.

## 2. Scope

### In Scope
- [x] Create `sysauto_script` scheduled job in **global** scope
- [x] Schedule: daily at 15:00 (3 PM)
- [x] Script: read-only GlideRecord query, limit 10, ordered by newest
- [x] New Update Set for metadata capture
- [x] Build, test, and document via pipeline

### Out of Scope
- Production deployment (human approval required)
- Modifying incident records
- Email/notification delivery of list
- Custom reporting or dashboard artifacts
- Flow Designer alternative (scheduled job explicitly requested)

## 3. Assumptions & Auto-Decisions

| # | Decision | Selected value | Source | Risk if wrong |
|---|----------|----------------|--------|---------------|
| 1 | Target instance | accenture-demo | DISCOVERY | Low |
| 2 | Update Set | `[20260617-090539-daily-incident-list-job] Daily Incident List Job` | DEFAULT | Low |
| 3 | Application scope | Global | USER + DEFAULT | Low |
| 4 | Job name | `[SN-DO] Daily Top 10 Incidents List` | DEFAULT | Low |
| 5 | Schedule type | `run_type=daily`, `run_time=1970-01-01 15:00:00` | USER + DEFAULT | Medium — timezone is instance default |
| 6 | Time zone | Instance default (empty `time_zone`) | DEFAULT | Medium — 3 PM follows instance TZ |
| 7 | Incident selection | 10 most recently created incidents, all states | DEFAULT | Low |
| 8 | Output method | `gs.info` log lines per incident | DEFAULT | Low |
| 9 | Job active on create | `active=true` | DEFAULT | Low — can deactivate for rollback |

## 4. Open Questions

| # | Question | Status | Resolution |
|---|----------|--------|------------|
| 1 | Which 10 incidents (filter)? | RESOLVED | Newest 10 by `sys_created_on` DESC, no state filter |
| 2 | Instance timezone for 3 PM? | WAIVED | Use instance default; document in deployment |

**Gate (autonomous mode)**: Proceed — no BLOCKING items.

## 5. Technical Design

### 5.1 Artifact plan

| # | Type | Name | Table | Action | When/Filter | MCP approach |
|---|------|------|-------|--------|-------------|--------------|
| 1 | Update Set | `[20260617-090539-daily-incident-list-job] Daily Incident List Job` | sys_update_set | CREATE | N/A | SN-Create-Record + BG script set current |
| 2 | Scheduled Script | `[SN-DO] Daily Top 10 Incidents List` | sysauto_script | CREATE | Daily 15:00 | SN-Create-Record |

### 5.2 Data model

No new fields. Read-only query on existing `incident` table.

### 5.3 Security & compliance

| Role | Access | Mechanism |
|------|--------|-----------|
| System (job runner) | Read incident | OOB ACLs for scheduled job context |

Script MUST NOT call `update()`, `insert()`, or `deleteRecord()`.

### 5.4 Lifecycle impact

| Module | States affected | Transitions | Required fields |
|--------|-----------------|-------------|-----------------|
| incident | None | None | N/A — read-only |

### 5.5 Integrations & dependencies

| Dependency | Name/sys_id | Step # |
|------------|-------------|--------|
| Incident table | incident | 2 |

## 6. Implementation Steps (ordered — Build Agent executes exactly)

| Step | Action | MCP Tool / Method | Expected Result | Verify By |
|------|--------|-------------------|-----------------|-----------|
| 0 | Verify instance + create/set Update Set | SN-Get-Current-Instance, SN-Create-Record (sys_update_set), SN-Execute-Background-Script | Current US = session US | SN-Get-Current-Update-Set / query sys_update_set |
| 1 | Create scheduled job | SN-Create-Record (sysauto_script) | Job exists, active, daily 15:00 | SN-Query-Table name=[SN-DO] Daily Top 10 Incidents List |
| 2 | Self-verify script content | SN-Get-Record / SN-Query-Table | Script contains GlideRecord read-only pattern, setLimit(10) | Query fields script, run_type, run_time, active |
| 3 | Inspect Update Set | SN-Inspect-Update-Set | sysauto_script component captured | SN-Inspect-Update-Set |

### Scheduled job script (canonical)

```javascript
// [SN-DO] Daily Top 10 Incidents List — read-only
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

### Scheduled job field values

| Field | Value |
|-------|-------|
| name | `[SN-DO] Daily Top 10 Incidents List` |
| active | true |
| run_type | daily |
| run_time | 1970-01-01 15:00:00 |
| time_zone | (empty) |
| conditional | false |
| script | (canonical script above) |

## 7. DO — Build Agent MUST

1. Follow steps in order; log to `build/implementation-log.md`
2. Write evidence to `build/evidence/step-N.md`
3. Self-verify each step before next
4. Ensure script is strictly read-only (no DML)
5. Capture job in Update Set before marking complete

## 8. DO NOT — Build Agent MUST NOT

1. Modify, insert, or delete incident records in the job script
2. Deploy to production via MCP
3. Create Flow Designer artifact (scheduled job requested)
4. Hardcode incident sys_ids
5. Deactivate OOB scheduled jobs

## 9. Acceptance Criteria (Testing Agent)

| AC# | Criterion | Test Method | Pass Condition | Type |
|-----|-----------|-------------|----------------|------|
| AC1 | Scheduled job exists with correct schedule | SN-Query-Table sysauto_script | name, active=true, run_type=daily, run_time contains 15:00:00 | happy |
| AC2 | Script execution is read-only | SN-Execute-Background-Script (run job script) + query incident sys_updated_on before/after | No incident sys_updated_on changes; script completes | negative |
| AC3 | No duplicate SN-DO job | SN-Query-Table name=[SN-DO] Daily Top 10 Incidents List | Exactly 1 active record | regression |
| AC4 | Update Set contains job | SN-Inspect-Update-Set | sysauto_script component present | happy |

## 10. Rollback Plan

| Artifact | Rollback action |
|----------|-----------------|
| Scheduled Script | Set `active=false` or delete record |
| Update Set | Back out / revert US on target env |

## 11. Deployment & post-deploy (human)

| Step | Action | Env |
|------|--------|-----|
| 1 | Complete Update Set | dev |
| 2 | Migrate to test | test |
| 3 | Verify job schedule in System Definition → Scheduled Jobs | test |
| 4 | Optional: run job once manually; check System Logs | test |
| 5 | Migrate to prod (human approval) | prod |

## 12. References

- Discovery notes: analyze/discovery-notes.md
- Platform catalog: Scheduled Script (`sysauto_script`)
- Tables: incident, sysauto_script, sys_update_set

---

**Sign-off**: READY FOR DEVELOPMENT
