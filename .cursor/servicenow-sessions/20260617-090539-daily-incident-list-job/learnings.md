# Session Learnings — 20260617-090539-daily-incident-list-job

Promoted to registry on 2026-06-17 (self-learning recheck).

| # | Type | Symptom | Root cause | Proposed fix | Status | Registry ID |
|---|------|---------|------------|--------------|--------|-------------|
| 1 | MCP_LIMITATION | REST create skipped sys_update_xml | GlideUpdateSet.set via separate trigger; REST path | Create metadata in same BG script as US set | PROMOTED | L001 |
| 2 | UX_COMMUNICATION | User asked why manual check needed | Conflated migration with delivery | "Done on dev" when functional pass | PROMOTED | L002 |
| 3 | BUILD_PATTERN | Scheduled job not in US | Same as L001 | BG script insert for sysauto_script | PROMOTED | L003 |
| 4 | TEST_PATTERN | AC4 BLOCKED lowered overall to PARTIAL | Packaging treated as functional | FUNCTIONAL vs PACKAGING AC classes | PROMOTED | L004 |
| 5 | BUILD_PATTERN | Read-only proof worked | Timestamp before/after compare | Standard test pattern L005 | PROMOTED | L005 |

## Promotion log

| Timestamp | Action | Files patched |
|-----------|--------|---------------|
| 2026-06-17 | Initial promotion from user recheck request | self-learning-protocol.md, learnings-registry.md, pipeline-gates.md, mcp-playbook.md, all agent SKILLs, sn-do, templates |

## Notes

- User feedback: "why do I need to manually check?" — drove L002 and UX updates across orchestrator, sn-do, documentation agent.
