# Revert Plan

**Revert ID**: 20260617-152024-revert-incident-service-mandatory  
**Source session**: 20260617-145813-incident-service-mandatory  
**Instance**: accenture-demo  
**User confirmed**: YES (explicit `/sn-revert <session_id>`)

## Inventory (from implementation-log)

| # | Artifact | Table | sys_id | Pipeline action | Revert action | Order |
|---|----------|-------|--------|-----------------|---------------|-------|
| 1 | business_service mandatory | sys_ui_policy_action | fd2e47d12ba1479015a9f5685e91bf62 | CREATE | mandatory=ignore | 1 |
| 2 | [SN-DO] Incident Service Mandatory - UI Policy | sys_ui_policy | 2d2e47d12ba1479015a9f5685e91bf42 | CREATE | active=false | 2 |
| 3 | business_service mandatory | sys_data_policy_rule | a92e47d12ba1479015a9f5685e91bf3c | CREATE | mandatory=false | 3 |
| 4 | [SN-DO] Incident Service Mandatory - Data Policy | sys_data_policy2 | 692e47d12ba1479015a9f5685e91bf0e | CREATE | active=false | 4 |
| 5 | Incident Service Mandatory Update Set | sys_update_set | ad2e07d12ba1479015a9f5685e91bfba | CREATE | state=ignore | 5 |

## Challenges

| Challenge | Status |
|-----------|--------|
| Migrated to prod | N/A — dev only, US was in progress |
| OOB artifacts | None in scope |
| Instance mismatch | None — accenture-demo matches |

## Out of scope

- Hard delete of any records
- Changes to OOB incident dictionary or form
- Pipeline files in `stories/` (preserved)
