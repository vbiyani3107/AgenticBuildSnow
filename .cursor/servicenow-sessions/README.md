# ServiceNow Session Folders

Each **story** gets one folder here when you run `/sn-analysis-agent` or `/sn-pipeline-orchestrator` in a new Cursor chat.

## Expected structure (created at bootstrap)

```
<session_id>/
├── SESSION.md
├── session.json
├── requirement/requirement.md
├── analyze/SPEC.md, handoff.md, discovery-notes.md
├── build/SPEC.md, implementation-log.md, evidence/
├── test/SPEC.md, test-report.md, evidence/
├── document/SPEC.md, jira-story.md
└── pipeline-execution-report.md   ← after full pipeline run
```

**Session ID format**: `YYYYMMDD-HHMMSS-<jira-or-slug>`

## Skills location

Personal skills: `~/.cursor/skills/`

| Skill | Invoke |
|-------|--------|
| Analysis | `/sn-analysis-agent` |
| Build | `/sn-development-agent` |
| Test | `/sn-testing-agent` |
| Document | `/sn-documentation-agent` |
| **SN Do (natural language)** | Say *"pipeline orchestrator …"* or `/sn-do` |
| **Full pipeline (engine)** | `/sn-pipeline-orchestrator` |

Index: `~/.cursor/skills/servicenow-spec-workflow/REFERENCE-INDEX.md`

## Note

Folders appear **after first analysis run** — this directory starts with INDEX.md only until you run a story.
