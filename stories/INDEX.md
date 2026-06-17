# ServiceNow Session Index

| Session ID | Jira | Title | Module | Status | Phase | Created | Path |
|------------|------|-------|--------|--------|-------|---------|------|
| 20260617-090539-daily-incident-list-job | SN-DO-SCHED-JOB | Daily incident list scheduled job | incident-management | completed | done | 2026-06-17 | `stories/20260617-090539-daily-incident-list-job/` |
| 20250617-120000-incident-new-field | INC-FIELD-DEMO | Add incident custom field | incident-management | in_progress | analysis done | 2026-06-17 | `stories/20250617-120000-incident-new-field/` |

## Remote development workflow

1. **New Cursor chat** per story
2. **`/sn-do`** or **`/sn-pipeline-orchestrator`** — full pipeline (recommended) OR run agents individually
3. `/sn-analysis-agent` — design only
4. `/sn-development-agent` — MCP build on dev
5. `/sn-testing-agent` — QA evidence
6. `/sn-documentation-agent` — Jira doc

**Skill index**: `~/.cursor/skills/servicenow-spec-workflow/REFERENCE-INDEX.md`

**Autonomous defaults**: when you don't answer analysis questions, agents apply ServiceNow best-practice defaults and document them in `analyze/handoff.md` §3.
