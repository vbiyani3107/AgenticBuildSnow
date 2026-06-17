# Test Phase — SPEC

**Session ID**: `{{SESSION_ID}}`  
**Phase**: test  
**Agent**: `sn-testing-agent`  
**Status**: pending

---

## Role

Independently verify acceptance criteria in `analyze/handoff.md`. Evidence required for every AC.

## Inputs

| Artifact | Path | Priority |
|----------|------|----------|
| Acceptance criteria | `analyze/handoff.md` §9 | **PRIMARY** |
| Implementation log | `build/implementation-log.md` | cross-check |
| Requirement | `requirement/requirement.md` | context |
| Phase spec | `test/SPEC.md` | this file |

## Outputs

| Artifact | Path |
|----------|------|
| Test report | `test/test-report.md` |
| AC evidence | `test/evidence/ac-<N>-<slug>.md` |
| Updated manifest | `SESSION.md`, `session.json` |

## Gate to next phase (document)

- [ ] Every AC has PASS / FAIL / BLOCKED with evidence
- [ ] Overall result documented
- [ ] `session.json` → `phases.test.overall_result` = PASS | PARTIAL | FAIL

| Result | Next action |
|--------|-------------|
| PASS | `/sn-documentation-agent` |
| FAIL/PARTIAL | `/sn-development-agent` rework, then re-test |

## MCP server

`user-servicenow-demo` — confirm same instance as build log.

## Test data convention

Prefix created records: `[TEST-{{SESSION_ID}}]` in short_description.

## Forbidden

Fix implementation; change ACs; mark PASS without independent MCP evidence.

---

*Phase spec for session {{SESSION_ID}}*
