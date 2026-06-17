# Daily Incident List Scheduled Job — Portable Artifact

Recreates the **`[SN-DO] Daily Top 10 Incidents List`** scheduled script on any ServiceNow instance.

## What it does

| Setting | Value |
|---------|-------|
| Table | `sysauto_script` |
| Scope | Global |
| Schedule | Daily at **3:00 PM** (instance local time) |
| Script | Read-only query — 10 newest incidents → `gs.info` log |

## Files

| File | Purpose |
|------|---------|
| `metadata.json` | Job name, sys_ids from dev, schedule, behavior |
| `sysauto_script-recreate.js` | Background script to create or update the job |

## Deploy to a new instance

### Option A — ServiceNow UI

1. Set your target **Update Set** (recommended for migration).
2. Go to **System Definition → Scripts - Background**.
3. Paste contents of `sysauto_script-recreate.js`.
4. Optionally set `UPDATE_SET_SYS_ID` at the top of the script.
5. Click **Run script**.
6. Verify: **System Definition → Scheduled Jobs** → filter name `[SN-DO] Daily Top 10 Incidents List`.
7. Optional: **Execute Now** → check **System Logs** for log lines starting with `[SN-DO] Daily Top 10 Incidents List:`.

### Option B — MCP (Cursor)

```
SN-Execute-Background-Script
  script: <contents of sysauto_script-recreate.js>
  description: Recreate daily incident list scheduled job
```

### Option C — Update existing job only

The script **upserts by name** — safe to re-run. It updates if the job already exists.

## Schedule / timezone

Default `RUN_TIME` is `1970-01-01 15:00:00` (ServiceNow daily job convention for 3 PM).

If the form shows a different local time after deploy, edit `RUN_TIME` in the script or on the scheduled job record to match your instance timezone.

## Source reference

| Item | Value |
|------|-------|
| Dev instance | accenture-demo |
| Source sys_id | `989d7d112b29c39015a9f5685e91bf91` |
| Session folder | `.cursor/servicenow-sessions/20260617-090539-daily-incident-list-job/` |

## Rollback

```javascript
var gr = new GlideRecord('sysauto_script');
gr.addQuery('name', '[SN-DO] Daily Top 10 Incidents List');
gr.query();
if (gr.next()) {
    gr.active = false;
    gr.update();
    // or: gr.deleteRecord();
}
```

## Related docs

- Full pipeline session: `../../.cursor/servicenow-sessions/20260617-090539-daily-incident-list-job/document/jira-story.md`
- Handoff design: `../../.cursor/servicenow-sessions/20260617-090539-daily-incident-list-job/analyze/handoff.md`
