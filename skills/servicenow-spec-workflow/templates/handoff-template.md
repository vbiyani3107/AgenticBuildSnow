# Handoff Document Template

**Session ID**: [from session.json]
**Session folder**: `.cursor/servicenow-sessions/<session_id>/`
**Story ID**: [JIRA-KEY or session slug]
**Title**: [One-line title]
**Module**: incident-management | change-management | problem-management | catalog | other
**SDLC phase at handoff**: Design complete → ready for Build
**Author (Analysis Agent)**: [date]
**Target Instance**: [SN-Get-Current-Instance]
**Handoff mode**: READY FOR DEVELOPMENT | DRAFT | BLOCKED
**Autonomous decisions**: [N] defaults applied — see §3

---

## 1. Requirement Summary

[2–4 sentences. Business need and outcome. No implementation detail.]

## 2. Scope

### In Scope
- [ ] Item 1

### Out of Scope
- Item excluded (default: prod deploy, bulk data migration, new catalog unless stated)

## 3. Assumptions & Auto-Decisions

| # | Decision | Selected value | Source | Risk if wrong |
|---|----------|----------------|--------|---------------|
| 1 | Target instance | [MCP instance] | DEFAULT / USER | |
| 2 | Update Set | [name] | DEFAULT / USER | |
| 3 | Test role | itil | DEFAULT | |

**Source values**: `USER` = user answered; `DEFAULT` = [default-decisions.md](../references/default-decisions.md); `DISCOVERY` = MCP query.

List every DEFAULT explicitly so user can correct later.

## 4. Open Questions

| # | Question | Status | Resolution |
|---|----------|--------|------------|
| 1 | | RESOLVED / WAIVED / BLOCKED | |

**Gate (autonomous mode)**: Proceed when BLOCKED = 0 OR only HARD STOP items remain documented with safe fallback. Do not block on NON-BLOCKING items.

## 5. Technical Design

### 5.1 Artifact plan

Use [platform-artifact-catalog.md](../references/platform-artifact-catalog.md) types.

| # | Type | Name | Table | Action | When/Filter | MCP approach |
|---|------|------|-------|--------|-------------|--------------|
| 1 | Assignment Rule | | sysrule_assignment | CREATE | | SN-Create-Record |
| 2 | UI Policy | | sys_ui_policy | CREATE | | SN-Batch-Create |

### 5.2 Data model

| Table | Field | Type | Mandatory | Notes |
|-------|-------|------|-----------|-------|

### 5.3 Security & compliance

| Role | Access | Mechanism |
|------|--------|-----------|
| itil | read/write fields | ACL |

Data policies for PII fields:

| Field | Policy |
|-------|--------|

### 5.4 Lifecycle impact

| Module | States affected | Transitions | Required fields |
|--------|-----------------|-------------|-----------------|
| incident | 1,2,6,7 | New→In Progress, →Resolved | close_code on resolve |

### 5.5 Integrations & dependencies

| Dependency | Name/sys_id | Step # |

## 6. Implementation Steps (ordered — Build Agent executes exactly)

| Step | Action | MCP Tool / Method | Expected Result | Verify By |
|------|--------|-------------------|-----------------|-----------|
| 0 | Instance + Update Set + scope | SN-Get-Current-Instance, SN-Set-Update-Set | US current | SN-Get-Current-Update-Set |
| 1 | | | | SN-Query-Table |

## 7. DO — Build Agent MUST

1. Follow steps in order; log to `build/implementation-log.md`
2. Write evidence to `build/evidence/step-N.md`
3. Self-verify each step before next
4. Apply assumptions in §3 when step is silent
5. Resolve groups/users/CIs by **name** via query — no hardcoded sys_ids

## 8. DO NOT — Build Agent MUST NOT

1. [Story-specific prohibitions]
2. Out of scope items (§2)
3. Modify OOB artifacts without handoff entry
4. Deploy to production via MCP
5. Create new Workflow (use Flow for new automation)
6. Put Business Rule on `task` when `incident` suffices

## 9. Acceptance Criteria (Testing Agent)

| AC# | Criterion | Test Method | Pass Condition | Type |
|-----|-----------|-------------|----------------|------|
| AC1 | | SN-Create-Incident + query | field X = Y | happy |
| AC2 | | create record not matching filter | no side effect | negative |
| AC3 | | query change_request | unchanged | regression |

Minimum: 1 happy + 1 negative + 1 regression per feature area.

## 10. Rollback Plan

| Artifact | Rollback action |
|----------|-----------------|
| Assignment Rule | Deactivate record |
| Update Set | Back out / revert US |

## 11. Deployment & post-deploy (human)

| Step | Action | Env |
|------|--------|-----|
| 1 | Complete Update Set | dev |
| 2 | Migrate to test | test |
| 3 | Execute Fix Script (if any) | test |
| 4 | Smoke test AC1–AC3 | test |
| 5 | Migrate to prod (human approval) | prod |

## 12. References

- Platform catalog: platform-artifact-catalog.md
- Module ref: incident-management.md (or other)
- Discovery notes: analyze/discovery-notes.md
- Tables:
- Related stories:

---

**Sign-off**: READY FOR DEVELOPMENT when design complete, ACs testable, steps ordered, assumptions documented.
