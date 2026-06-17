# Revert Session Protocol

Reverts are **separate from pipeline sessions**. One revert run = one folder under `reverts/`.

## Relationship to pipeline

```
stories/<session_id>/          ← pipeline artifacts (never deleted by revert agent)
    build/implementation-log.md  ← inventory source
    session.json                 ← artifact sys_ids + instance

reverts/<revert_id>/           ← revert run artifacts
    revert.json                  ← points to source_session_id
```

## Revert ID format

```
YYYYMMDD-HHMMSS-revert-<source-session-slug>
```

Example: `20260617-160000-revert-incident-service-mandatory`

## Folder layout (mandatory)

```
reverts/<revert_id>/
├── REVERT.md              ← Human index (read first)
├── revert.json            ← Machine manifest
├── revert-plan.md         ← Pre-execute plan (shown to user)
├── revert-report.md       ← Post-execute report
└── evidence/              ← Per-step verification
    └── step-0.md
```

## revert.json contract

```json
{
  "schema_version": "1.0",
  "revert_id": "<revert_id>",
  "source_session_id": "<pipeline session_id>",
  "source_session_root": "stories/<session_id>",
  "created_at": "<ISO8601>",
  "completed_at": null,
  "status": "planned|in_progress|completed|partial|blocked",
  "instance": { "name": "", "url": "" },
  "revert_update_set": { "name": null, "sys_id": null },
  "artifacts_planned": 0,
  "artifacts_reverted": 0,
  "artifacts_skipped": 0,
  "user_confirmed": false,
  "paths": {
    "revert_root": "reverts/<revert_id>",
    "plan": "revert-plan.md",
    "report": "revert-report.md",
    "evidence_dir": "evidence"
  }
}
```

## Gates

| Gate | Rule |
|------|------|
| G-R0 | Source session exists with `build/implementation-log.md` |
| G-R1 | Revert plan lists only pipeline artifacts |
| G-R2 | User confirmed plan (or explicit revert intent) |
| G-R3 | Instance matches session.json |
| G-R4 | Every planned artifact verified `active=false` or SKIPPED with reason |
| G-R5 | `revert-report.md` written |

## Workspace index

`reverts/INDEX.md` — one row per revert run (like `stories/INDEX.md`).

## Non-destructive rules

| DO | DON'T |
|----|-------|
| Append revert note to `stories/<id>/SESSION.md` | Delete pipeline session folder |
| Add `revert` block to `session.json` | Remove build/test evidence |
| Create new files under `reverts/` | Overwrite `implementation-log.md` |
