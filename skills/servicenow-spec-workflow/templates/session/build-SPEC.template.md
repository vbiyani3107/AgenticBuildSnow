# Build Phase — SPEC

**Session ID**: `{{SESSION_ID}}`  
**Phase**: build  
**Agent**: `sn-development-agent`  
**Status**: pending

---

## Role

Execute `analyze/handoff.md` exactly via MCP. Self-verify each step. Log everything.

## Inputs (read before any MCP write)

| Artifact | Path | Priority |
|----------|------|----------|
| Handoff (binding law) | `analyze/handoff.md` | **PRIMARY** |
| Requirement (context) | `requirement/requirement.md` | secondary |
| Test gaps (rework only) | `test/test-report.md` | rework only |
| Phase spec | `build/SPEC.md` | this file |
| MCP playbook | `~/.cursor/skills/sn-development-agent/mcp-playbook.md` | reference |

## Outputs (must write)

| Artifact | Path |
|----------|------|
| Implementation log | `build/implementation-log.md` |
| Step evidence | `build/evidence/step-<N>-<slug>.md` (one per completed step) |
| Updated manifest | `SESSION.md`, `session.json` |

## Gate to next phase (test)

- [ ] All handoff implementation steps DONE or BLOCKED with reason
- [ ] Self-verification PASS for each completed step
- [ ] Update Set inspection logged (if metadata changed)
- [ ] `session.json` → `phases.build.status` = `completed`, `ready_for_testing` = true

## MCP server

`user-servicenow-demo` — always `SN-Get-Current-Instance` first.

## Rework mode

When `test/test-report.md` has FAIL gaps:
1. Read Failures & Gaps section only
2. Append `## Rework Run [timestamp]` to implementation log
3. Increment `session.json` → `phases.build.rework_count`

## Forbidden

Implement out-of-scope items; skip self-verification; run full AC test suite (Test Agent's job).

---

*Phase spec for session {{SESSION_ID}}*
