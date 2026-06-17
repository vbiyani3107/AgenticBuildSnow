# Revert Report

**Revert ID**: 20260617-152024-revert-incident-service-mandatory  
**Source session**: 20260617-145813-incident-service-mandatory  
**Title**: Make Service field mandatory on incident form  
**Instance**: accenture-demo  
**Date**: 2026-06-17T15:20:24Z  
**Result**: SUCCESS  
**User confirmed**: YES

---

## Summary

All pipeline-delivered policies for mandatory Service (`business_service`) on incident were deactivated on dev. Service is optional again; incident save without Service succeeds.

## Source inventory

| # | Type | Name | sys_id | Pipeline action |
|---|------|------|--------|-----------------|
| 1 | UI Policy Action | business_service mandatory | fd2e47d12ba1479015a9f5685e91bf62 | CREATE |
| 2 | UI Policy | [SN-DO] Incident Service Mandatory - UI Policy | 2d2e47d12ba1479015a9f5685e91bf42 | CREATE |
| 3 | Data Policy Rule | business_service mandatory | a92e47d12ba1479015a9f5685e91bf3c | CREATE |
| 4 | Data Policy | [SN-DO] Incident Service Mandatory - Data Policy | 692e47d12ba1479015a9f5685e91bf0e | CREATE |
| 5 | Update Set | [20260617-145813-incident-service-mandatory] Incident Service Mandatory | ad2e07d12ba1479015a9f5685e91bfba | CREATE |

## Revert execution

| # | Artifact | Action | Result | Evidence |
|---|----------|--------|--------|----------|
| 1 | UI Policy Action | mandatory=ignore | PASS | evidence/step-0.md |
| 2 | UI Policy | active=false | PASS | evidence/step-1.md |
| 3 | Data Policy Rule | mandatory=false | PASS | evidence/step-2.md |
| 4 | Data Policy | active=false | PASS | evidence/step-3.md |
| 5 | Source Update Set | state=ignore | PASS | evidence/step-4.md |

## Challenges encountered

None. Session was dev-only; no prod migration detected.

## Verification

| Check | Result |
|-------|--------|
| All policies inactive / rule reverted | PASS |
| Incident create without business_service | PASS (INC0014729) |

## Remaining active artifacts

None from pipeline scope. Records still exist (deactivated, not deleted) — recoverable by setting active=true.

## Update Set

| Field | Value |
|-------|-------|
| Revert US name | [20260617-152024-revert-incident-service-mandatory] Revert Service Mandatory |
| sys_id | 9d031b952be1479015a9f5685e91bf76 |

## Rollback of this revert

Re-enable policies: set active=true on UI Policy and Data Policy sys_ids; restore mandatory on child rules/actions; or re-run `/sn-do` for the original requirement.

---

*Pipeline history preserved at `stories/20260617-145813-incident-service-mandatory/`.*
