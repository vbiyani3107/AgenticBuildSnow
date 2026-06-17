# AgenticBuildSnow

Agentic ServiceNow development workflow for Cursor — natural-language requests run through a full **Analyze → Build → Test → Document** pipeline with MCP integration on a dev instance.

## What this repo contains

```
AgenticBuildSnow/
├── stories/           ← Your ServiceNow stories (pipeline artifacts)
├── artifacts/         ← Portable deploy scripts (recreate on any instance)
├── skills/            ← sn-do pipeline skills + spec workflow
└── .cursor/
    └── rules/         ← Cursor-only: route SN requests to sn-do
```

| Path | Purpose |
|------|---------|
| `stories/` | **Per-story folders** — requirements, handoff, build log, tests, docs |
| `artifacts/` | Portable deploy scripts to recreate ServiceNow config on other instances |
| `skills/` | Cursor agent skills (`sn-do`, orchestrator, analysis/build/test/document, spec workflow) |
| `.cursor/rules/` | Workspace rule to auto-route ServiceNow requests to `sn-do` |

## Quick start

1. Copy or symlink `skills/*` to `~/.cursor/skills/` (or reference from your Cursor skills path).
2. Enable MCP server `user-servicenow-demo` pointing at your ServiceNow dev instance.
3. In Cursor, say for example:

```
/sn-do create a global scheduled job to run daily at 3 PM and list 10 incidents (read-only)
```

## Pipeline phases

| Phase | Skill | Output |
|-------|-------|--------|
| Analyze | `sn-analysis-agent` | `analyze/handoff.md` |
| Build | `sn-development-agent` | `build/implementation-log.md` |
| Test | `sn-testing-agent` | `test/test-report.md` |
| Document | `sn-documentation-agent` | `document/jira-story.md` |

Entry point: **`sn-do`** (natural language) or **`sn-pipeline-orchestrator`** (engine).

## Self-learning

The workflow captures learnings per session (`learnings.md`) and promotes patterns to `skills/servicenow-spec-workflow/references/learnings-registry.md`. See `self-learning-protocol.md` in that folder.

## Example sessions

| Session | Story | Portable artifact |
|---------|-------|-------------------|
| `20260617-090539-daily-incident-list-job` | Daily scheduled job — list top 10 incidents (read-only) at 3 PM | `artifacts/daily-incident-list-job/` |
| `20250617-120000-incident-new-field` | Incident custom field (analysis) | — |

## Related

The ServiceNow MCP connector may live in a sibling project (`demoenvservicenowmcp/`) — not included here (separate repository).

## License

Internal / demo use — adjust as needed for your organization.
