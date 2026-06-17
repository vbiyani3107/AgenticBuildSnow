# Analyze Phase — SPEC

**Session ID**: `{{SESSION_ID}}`  
**Phase**: analyze  
**Agent**: `sn-analysis-agent`  
**Status**: in_progress

---

## Role

SDLC Intake + Design. Produce binding `analyze/handoff.md`. **Autonomous**: apply defaults if user silent.

## References (read)

- `default-decisions.md` — auto-answers
- `platform-artifact-catalog.md` — artifact types
- `sdlc-remote-development.md` — SDLC alignment
- Module: `incident-management.md` | `change-management.md` | `problem-management.md`

## Inputs

| Artifact | Path |
|----------|------|
| Requirement | `requirement/requirement.md` |
| Manifest | `SESSION.md`, `session.json` |

## Outputs

| Artifact | Path |
|----------|------|
| Handoff | `analyze/handoff.md` |
| Discovery | `analyze/discovery-notes.md` |
| Manifests | `SESSION.md`, `session.json` |

## Gate → build

- [ ] handoff **READY FOR DEVELOPMENT**
- [ ] §3 Assumptions documented (every DEFAULT)
- [ ] §9 ACs: happy + negative + regression
- [ ] §6 ordered steps with MCP + verify
- [ ] `phases.analyze.status` = completed

## MCP (read-only only)

Discovery tools per sn-analysis-agent skill.

---

*Phase spec — session {{SESSION_ID}}*
