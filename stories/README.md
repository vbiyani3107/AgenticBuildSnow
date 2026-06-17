# Stories — ServiceNow delivery record

Each **story** (one Cursor chat / one pipeline run) gets one folder here. This is your **project work** — requirements, design, build evidence, tests, and documentation — not Cursor IDE configuration.

`.cursor/` holds only **rules** that route chat to `sn-do`. **Stories live here at repo root.**

## Folder structure (per story)

```
stories/<session_id>/
├── SESSION.md
├── session.json
├── learnings.md                  ← self-learning capture (promoted to skills registry)
├── requirement/requirement.md
├── analyze/SPEC.md, handoff.md, discovery-notes.md
├── build/SPEC.md, implementation-log.md, evidence/
├── test/SPEC.md, test-report.md, evidence/
├── document/SPEC.md, jira-story.md
└── pipeline-execution-report.md  ← after full pipeline run
```

**Session ID format**: `YYYYMMDD-HHMMSS-<jira-or-slug>`

## Index

See [INDEX.md](INDEX.md) for all stories in this workspace.

## Portable deploy

Reusable ServiceNow config (scripts to run on other instances) lives in [`../artifacts/`](../artifacts/) — not inside each story folder.

## Skills

Pipeline skills: [`../skills/`](../skills/) in this repo (copy to `~/.cursor/skills/` for Cursor).

| Skill | Invoke |
|-------|--------|
| **SN Do** | `/sn-do` or *"pipeline orchestrator …"* |
| Analysis | `/sn-analysis-agent` |
| Build | `/sn-development-agent` |
| Test | `/sn-testing-agent` |
| Document | `/sn-documentation-agent` |
| **Revert** (separate) | `/sn-revert` or `/sn-revert-agent` |

Index: [`../skills/servicenow-spec-workflow/REFERENCE-INDEX.md`](../skills/servicenow-spec-workflow/REFERENCE-INDEX.md)

## Revert runs (separate from pipeline)

Rollback of a pipeline session is **not** a pipeline phase. Output lives in [`../reverts/`](../reverts/) — see [`../reverts/README.md`](../reverts/README.md).
