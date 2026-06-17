# Session Protocol — One Story = One Cursor Session = One Folder

Every ServiceNow story runs in an **isolated session folder**. One Cursor chat window maps to exactly one session. All four agents resolve artifacts through `session.json` — never guess paths.

## Session identity

| Concept | Rule |
|---------|------|
| New story | User starts a **new Cursor chat** → Analysis Agent bootstraps a **new session folder** |
| Same story, rework | **Same chat** → reuse existing session; append rework sections to build log |
| Wrong session | STOP if `session.json` session_id does not match user intent |

## Session ID format

```
YYYYMMDD-HHMMSS-<jira-or-slug>
```

Examples:
- `20250617-143022-INC-1234-network-assign`
- `20250617-091500-p1-escalation-email`

Generate at bootstrap: current UTC/local timestamp + kebab-case slug (max 30 chars). Jira key preferred over title slug.

## Folder layout (mandatory)

```
.cursor/servicenow-sessions/<session_id>/
├── SESSION.md              ← Human manifest — read first in every agent run
├── session.json            ← Machine manifest — canonical path resolver
├── requirement/
│   └── requirement.md      ← Verbatim user requirement
├── analyze/
│   ├── SPEC.md             ← Phase contract for Analysis Agent
│   ├── handoff.md          ← Binding spec for Build Agent
│   └── discovery-notes.md  ← Optional MCP read-only findings
├── build/
│   ├── SPEC.md             ← Phase contract for Build Agent
│   ├── implementation-log.md
│   └── evidence/           ← Per-step verification snapshots
├── test/
│   ├── SPEC.md
│   ├── test-report.md
│   └── evidence/
├── document/
│   ├── SPEC.md
│   └── jira-story.md
└── learnings.md            ← Session learnings (promoted to registry)
```

## Bootstrap (Analysis Agent only)

When starting a **new story** in a **new Cursor session**:

1. Generate `session_id`
2. Create full tree above (empty evidence dirs included)
3. Write `session.json` and `SESSION.md` from templates
4. Write phase `SPEC.md` for all four phases (populate session_id, jira_key, title)
5. Save requirement to `requirement/requirement.md`
6. Set `current_phase: "analyze"`, `status: "in_progress"`

**Never** reuse an existing session folder for a different requirement.

## Session resolution (every agent, every run)

Execute in order:

```
1. If user gives explicit session path or session_id → use it
2. Else if exactly one session.json has "active": true in workspace → use it
3. Else if Analysis Agent and user pasted new requirement → bootstrap new session (step above)
4. Else list recent sessions from .cursor/servicenow-sessions/*/session.json → ask user to pick
5. Never read/write artifacts outside resolved session_root
```

## session.json contract

All paths in `session.json` are **relative to session_root**. Agents join: `{session_root}/{relative_path}`.

After each phase completes, the agent MUST update `session.json`:
- `current_phase` → next phase
- `phases.<phase>.status` → `pending|in_progress|completed|blocked`
- `updated_at` → ISO-8601

## Phase gates (via session.json)

| Transition | Gate |
|------------|------|
| analyze → build | `phases.analyze.status` = completed; handoff READY FOR DEVELOPMENT |
| build → test | `phases.build.status` = completed; implementation log exists |
| test → document | test PASS or user accepts PARTIAL |
| test FAIL → build | append build rework; set `phases.test.status` = blocked |

## SESSION.md contract

`SESSION.md` is the human-readable index. Keep in sync with `session.json` after every phase.

## Cross-session isolation

| DO | DON'T |
|-----|--------|
| Read only within resolved session | Mix artifacts across sessions |
| Pass session_id in every agent completion message | Hardcode artifact paths in chat without session.json |

## Active session flag

Only **one** session should have `"active": true` per workspace at a time.

Analysis bootstrap sets `"active": true`. Documentation completion or explicit user close sets `"active": false`, `status: "completed"`.

## Rework within same session

Test FAIL → Build appends `## Rework Run [timestamp]` to `build/implementation-log.md`; update session.json `phases.build.rework_count` and `phases.test.status` = `blocked` until retest passes.

## Scalability

- **Module scale**: add `references/<module>.md`; set `session.json` `module` field.
- **Many sessions**: each story = one folder; never delete sessions — archive with `status: "archived"` when done.

## Autonomous remote development

Agents **do not block** when user does not answer non-critical questions. Analysis applies [default-decisions.md](default-decisions.md), documents in handoff §3, proceeds to READY.

| Phase | Autonomous behavior |
|-------|---------------------|
| Analyze | Ask once → defaults → READY with §3 filled |
| Build | Execute handoff + §3 assumptions |
| Test | Run all ACs; BLOCKED = manual UI steps documented |
| Document | Truthful doc including defaults and gaps |

**Production deploy** always requires human — MCP targets dev/subprod only by default.

## Agent completion checklist

Before finishing any agent run:

- [ ] Read `SESSION.md` and `session.json`
- [ ] Wrote deliverable(s) to paths declared in session.json
- [ ] Updated session.json phase status and `updated_at`

## Legacy migration

Flat `.cursor/servicenow-artifacts/<slug>/` is **deprecated** — do not create new sessions in old layout.

## Workspace index

Optional: `.cursor/servicenow-sessions/INDEX.md` lists all sessions (session_id, title, status, current_phase, created_at) — Documentation Agent or Analysis bootstrap appends one row per new session.
