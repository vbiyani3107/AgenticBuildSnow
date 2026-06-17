# Revert Report

**Revert ID**: <revert_id>  
**Source session**: <session_id>  
**Title**: <story title>  
**Instance**: <instance name>  
**Date**: <ISO8601>  
**Result**: SUCCESS | PARTIAL | BLOCKED  
**User confirmed**: YES | NO

---

## Summary

<1–2 sentences: what was reverted and outcome>

## Source inventory

From `stories/<session_id>/build/implementation-log.md`:

| # | Type | Name | sys_id | Pipeline action |
|---|------|------|--------|-----------------|
| 1 | | | | CREATE |

## Revert execution

| # | Artifact | Action | Result | Evidence |
|---|----------|--------|--------|----------|
| 1 | | deactivate | PASS / SKIPPED / FAIL | evidence/step-N.md |

## Challenges encountered

| Challenge | Resolution |
|-----------|------------|
| | |

## Verification

| Check | Result |
|-------|--------|
| All planned artifacts inactive | PASS / FAIL |
| Functional smoke test | PASS / SKIPPED / FAIL |

## Remaining active artifacts

<List any pipeline artifacts user chose not to revert, or SKIPPED items>

## Update Set

| Field | Value |
|-------|-------|
| Revert US name | |
| sys_id | |
| Note | Revert US captures deactivations for audit |

## Rollback of this revert

To re-enable: set `active=true` on listed sys_ids in reverse order (parents after children), or re-run pipeline build for session.

---

*Pipeline history preserved at `stories/<session_id>/`. This report lives at `reverts/<revert_id>/`.*
