# Session Manifest

> **Session ID**: `{{SESSION_ID}}`  
> **Status**: `in_progress` | **Phase**: `analyze`  
> **Jira**: {{JIRA_KEY}} — {{TITLE}}  
> **Module**: Incident Management  
> **Created**: {{ISO8601_CREATED}}

This file is the **single human index** for this Cursor session. Every agent reads this first, then `session.json` for machine paths.

---

## Quick navigation

| Phase | Agent | Spec | Deliverable | Status |
|-------|-------|------|-------------|--------|
| Requirement | — | — | [requirement/requirement.md](requirement/requirement.md) | captured |
| Analyze | `/sn-analysis-agent` | [analyze/SPEC.md](analyze/SPEC.md) | [analyze/handoff.md](analyze/handoff.md) | pending |
| Build | `/sn-development-agent` | [build/SPEC.md](build/SPEC.md) | [build/implementation-log.md](build/implementation-log.md) | pending |
| Test | `/sn-testing-agent` | [test/SPEC.md](test/SPEC.md) | [test/test-report.md](test/test-report.md) | pending |
| Document | `/sn-documentation-agent` | [document/SPEC.md](document/SPEC.md) | [document/jira-story.md](document/jira-story.md) | pending |

**Machine manifest**: [session.json](session.json)

---

## Requirement summary

[1–2 sentences — filled by Analysis Agent after reading requirement/requirement.md]

---

## Phase pipeline

```
requirement/requirement.md
    → analyze/handoff.md          (binding spec)
    → build/implementation-log.md
    → test/test-report.md
    → document/jira-story.md      (Jira artifact)
```

**Rework loop**: test FAIL → build (append rework) → test again (same session folder).

---

## Instance & deployment context

| Field | Value |
|-------|-------|
| Target instance | TBD |
| Update Set | TBD |
| Application scope | TBD |

---

## Open items (session-level)

| # | Item | Owner | Status |
|---|------|-------|--------|

---

## Session log

| Timestamp | Phase | Event |
|-----------|-------|-------|
| {{ISO8601_CREATED}} | bootstrap | Session created |

---

*Keep this file synchronized with session.json after every agent run.*
