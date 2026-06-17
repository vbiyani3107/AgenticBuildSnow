# Handoff Document

**Session ID**: 20260617-145813-incident-service-mandatory  
**Session folder**: `stories/20260617-145813-incident-service-mandatory/`  
**Story ID**: SN-DO-SERVICE-MAND  
**Title**: Make Service field mandatory on incident form  
**Module**: incident-management  
**SDLC phase at handoff**: Design complete → ready for Build  
**Author (Analysis Agent)**: 2026-06-17  
**Target Instance**: accenture-demo (https://accentureservicessrodemo4.service-now.com)  
**Handoff mode**: READY FOR DEVELOPMENT  
**Autonomous decisions**: 6 defaults applied — see §3

---

## 1. Requirement Summary

Make the **Service** field (`business_service`) mandatory when creating or updating incidents on the classic form. Users must select a business service before saving; server-side validation must reject saves without a value.

## 2. Scope

### In Scope
- [x] UI Policy + UI Policy Action on `incident` — client mandatory (red asterisk)
- [x] Data Policy + Data Policy Rule on `incident` — server mandatory
- [x] New Update Set for migration packaging
- [x] Classic incident form (default view)

### Out of Scope
- Agent Workspace / Next Experience layout changes
- Change request, problem, or other task types
- Dictionary-level `mandatory=true` on `task` (would affect all task tables)
- Production deployment

## 3. Assumptions & Auto-Decisions

| # | Decision | Selected value | Source | Risk if wrong |
|---|----------|----------------|--------|---------------|
| 1 | Target instance | accenture-demo | DISCOVERY | Low |
| 2 | Update Set | `[20260617-145813-incident-service-mandatory] Incident Service Mandatory` | DEFAULT | Low |
| 3 | Field API name | `business_service` (label: Service) | DISCOVERY | Low |
| 4 | Enforcement pattern | UI Policy + Data Policy (not dictionary) | DEFAULT | Low — incident-only scope |
| 5 | UI surface | Classic incident form | DEFAULT | Medium — Workspace may differ |
| 6 | Conditions | Always mandatory (no state filter) | DEFAULT | Low |
| 7 | Test role | itil | DEFAULT | Low |

## 4. Open Questions

| # | Question | Status | Resolution |
|---|----------|--------|------------|
| — | None | — | — |

## 5. Technical Design

### 5.1 Artifact plan

| # | Type | Name | Table | Action | When/Filter | MCP approach |
|---|------|------|-------|--------|-------------|--------------|
| 1 | Update Set | [20260617-145813-incident-service-mandatory] Incident Service Mandatory | sys_update_set | CREATE | — | BG script |
| 2 | Data Policy | [SN-DO] Incident Service Mandatory - Data Policy | sys_data_policy2 | CREATE | model_table=incident | BG script |
| 3 | Data Policy Rule | business_service mandatory | sys_data_policy_rule | CREATE | field=business_service | BG script |
| 4 | UI Policy | [SN-DO] Incident Service Mandatory - UI Policy | sys_ui_policy | CREATE | table=incident, always | BG script |
| 5 | UI Policy Action | business_service mandatory | sys_ui_policy_action | CREATE | field=business_service | BG script |

### 5.2 Data model

| Table | Field | Type | Mandatory | Notes |
|-------|-------|------|-----------|-------|
| incident | business_service | reference (cmdb_ci_service) | via policy | Inherited from task dictionary |

### 5.3 Security & compliance

No new ACLs. Existing itil access unchanged.

### 5.4 Lifecycle impact

| Module | States affected | Transitions | Required fields |
|--------|-----------------|-------------|-----------------|
| incident | All (1–8) | New, In Progress, On Hold, Resolved, Closed | business_service on save |

## 6. Implementation Steps

| Step | Action | Expected Result | Verify |
|------|--------|-----------------|--------|
| 0 | Create Update Set + set current | US in progress, current for user | Query sys_update_set |
| 1 | Create Data Policy + Rule | DP active, rule mandatory=true for business_service | Query sys_data_policy2, sys_data_policy_rule |
| 2 | Create UI Policy + Action | UI policy active, action mandatory=true | Query sys_ui_policy, sys_ui_policy_action |
| 3 | Inspect Update Set | Components captured (best effort) | SN-Inspect-Update-Set |

## 7. DO (Build)

- Use single background script with GlideUpdateSet.set() per L001/L003
- Idempotent create (query by name before insert)
- Log all sys_ids in implementation-log

## 8. DO NOT (Build)

- Do not set dictionary mandatory on `task` table
- Do not create Business Rule for mandatory validation
- Do not modify OOB UI policies

## 9. Acceptance Criteria

| AC | Type | Description | Verify |
|----|------|-------------|--------|
| AC-1 | FUNCTIONAL | Data Policy exists, active, model_table=incident, business_service rule mandatory=true | MCP query |
| AC-2 | FUNCTIONAL | UI Policy exists, active, table=incident, action mandatory for business_service | MCP query |
| AC-3 | FUNCTIONAL | Incident insert without business_service rejected server-side | BG script insert test |
| AC-4 | PACKAGING | Update Set contains policy artifacts | SN-Inspect-Update-Set |

## 10. Rollback

| Artifact | Rollback |
|----------|----------|
| UI Policy | Set active=false or delete |
| Data Policy | Set active=false or delete |
| Update Set | Revert or complete without migration |

## 11. Deployment

Human: complete Update Set → migrate to test/prod → verify incident form shows red asterisk on Service.
