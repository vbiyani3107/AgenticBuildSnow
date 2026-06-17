# ServiceNow Revert Runs

This folder holds **revert agent** output — separate from pipeline sessions in `stories/`.

## When to use

After a pipeline session (`/sn-do`) delivered work you want to undo:

```
/sn-revert 20260617-145813-incident-service-mandatory

/sn-revert-agent undo the service mandatory session

revert last pipeline session
```

Skill: `~/.cursor/skills/sn-revert-agent/SKILL.md`

## Layout

```
reverts/
├── INDEX.md
├── README.md
└── <revert_id>/
    ├── REVERT.md
    ├── revert.json
    ├── revert-plan.md      ← shown before execute
    ├── revert-report.md    ← outcome + evidence
    └── evidence/
```

## Safety rules

- Reverts **only** artifacts listed in the source session's `build/implementation-log.md`
- Default action: **deactivate** (`active=false`) — not hard delete
- Pipeline history in `stories/` is **never deleted** — only a revert note is appended

## Relationship

| Folder | Purpose |
|--------|---------|
| `stories/<session_id>/` | Pipeline deliverables (analyze, build, test, document) |
| `reverts/<revert_id>/` | Rollback run tied to one source session |

See skill: `sn-revert-agent/references/revert-session-protocol.md`
