# Document Phase — SPEC

**Session ID**: `{{SESSION_ID}}`  
**Phase**: document  
**Agent**: `sn-documentation-agent`  
**Status**: pending

---

## Role

Synthesize all session artifacts into Jira-ready documentation. Document truthfully — include failures.

## Inputs (read all)

| Artifact | Path |
|----------|------|
| Requirement | `requirement/requirement.md` |
| Handoff | `analyze/handoff.md` |
| Implementation log | `build/implementation-log.md` |
| Test report | `test/test-report.md` |
| Session manifest | `SESSION.md`, `session.json` |

## Outputs

| Artifact | Path |
|----------|------|
| Jira story doc | `document/jira-story.md` |
| Updated manifest | `SESSION.md`, `session.json` |

## Gate to session complete

- [ ] `document/jira-story.md` complete with Jira paste block
- [ ] `session.json` → `phases.document.status` = `completed`, `status` = `completed`, `active` = false
- [ ] Append row to `stories/INDEX.md`

## Preconditions

Prefer test **PASS** or user accepts PARTIAL. If test missing → banner "Testing not completed".

## Forbidden

Invent work not in logs; hide test failures; modify ServiceNow instance.

---

*Phase spec for session {{SESSION_ID}}*
