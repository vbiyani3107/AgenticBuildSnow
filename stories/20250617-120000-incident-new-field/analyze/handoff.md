# Handoff Document

**Session ID**: `20250617-120000-incident-new-field`  
**Session folder**: `stories/20250617-120000-incident-new-field/`  
**Story ID**: INC-FIELD-DEMO  
**Title**: Add new custom field to Incident form  
**Module**: incident-management  
**SDLC phase at handoff**: Design complete → ready for Build (pending field spec from user)  
**Author (Analysis Agent)**: 2026-06-17  
**Target Instance**: accenture-demo (https://accentureservicessrodemo4.service-now.com)  
**Handoff mode**: **DRAFT** — field name, type, and placement not specified by user  
**Autonomous decisions**: 6 defaults applied for design skeleton — see §3

---

## 1. Requirement Summary

Add a new field to the Incident form on the connected dev instance. User did not specify field label, API name, type, mandatory rules, or form placement. This handoff provides a **complete SN-compliant design pattern** using placeholder values marked for user confirmation before Build.

**Analysis-only run**: Build/Test/Document phases were **not executed**.

---

## 2. Scope

### In Scope
- [ ] New dictionary entry on `incident` table
- [ ] Form layout — place field on classic Incident form
- [ ] ACLs for new field (read/write for itil)
- [ ] Update Set capture of all metadata
- [ ] Agent Workspace consideration (document if separate layout needed)

### Out of Scope
- [ ] Production deployment
- [ ] Bulk data population on existing incidents
- [ ] Business Rules / Flows (unless field is mandatory on resolve — TBD)
- [ ] Catalog / Portal changes

---

## 3. Assumptions & Auto-Decisions

| # | Decision | Selected value | Source | Risk if wrong |
|---|----------|----------------|--------|---------------|
| 1 | Target instance | accenture-demo | DISCOVERY | Low |
| 2 | Update Set name | `[INC-FIELD-DEMO] Add incident custom field` | DEFAULT | Low |
| 3 | Field API name (placeholder) | `u_demo_custom_field` | DEFAULT — **user must confirm** | High |
| 4 | Field label (placeholder) | `Demo Custom Field` | DEFAULT — **user must confirm** | High |
| 5 | Field type (placeholder) | `string`, max length 255 | DEFAULT — **user must confirm** | High |
| 6 | Mandatory | No (optional field) | DEFAULT | Medium |
| 7 | Form placement | Classic form — "Additional info" or new section | DEFAULT | Medium |
| 8 | Test role | itil | DEFAULT | Low |
| 9 | Scoped app | Global (OOB incident table) | DEFAULT | Medium |

---

## 4. Open Questions

| # | Question | Status | Resolution |
|---|----------|--------|------------|
| 1 | What is the **field label** and **API name**? | **BLOCKING** | Pending user |
| 2 | What **field type**? (string, integer, choice, reference, date, etc.) | **BLOCKING** | Pending user |
| 3 | **Mandatory**? On which states? | NON-BLOCKING | Default: optional |
| 4 | **Agent Workspace** layout required or classic only? | NON-BLOCKING | Default: classic first |
| 5 | If **choice** or **reference** — choices/reference table? | BLOCKING if type=choice/reference | Pending user |
| 6 | Any **UI Policy** (show when state=X)? | NON-BLOCKING | Default: none |

**Gate (strict pipeline)**: Build must **NOT** start until Q1, Q2 resolved (and Q5 if applicable).

---

## 5. Technical Design

### 5.1 Artifact plan

| # | Type | Name | Table | Action | Notes |
|---|------|------|-------|--------|-------|
| 1 | Dictionary | `u_demo_custom_field` | sys_dictionary | CREATE | On incident; replace name when user confirms |
| 2 | Form layout | Incident form element | sys_ui_element | CREATE | Via form design or sys_ui_element record |
| 3 | ACL | incident.u_demo_custom_field | sys_security_acl | CREATE | read/write for itil |
| 4 | ACL | incident.u_demo_custom_field | sys_security_acl | CREATE | read for sn_incident_read (optional) |

**SN best practice**: Dictionary creates column; form layout exposes on UI; ACLs secure access.

### 5.2 Data model

| Table | Field | Type | Mandatory | Notes |
|-------|-------|------|-----------|-------|
| incident | u_demo_custom_field | string(255) | No | PLACEHOLDER — confirm with user |

### 5.3 Security

| Role | Access | Mechanism |
|------|--------|-----------|
| itil | read, write | Field ACL |
| admin | implicit | — |

No PII assumed — if field holds PII, add Data Policy in Build after user confirms.

### 5.4 Lifecycle impact

| Module | States affected | Notes |
|--------|-----------------|-------|
| incident | All | Optional field — no state transition change unless mandatory rule added |

### 5.5 Integrations

None.

---

## 6. Implementation Steps (for Build Agent — not executed)

| Step | Action | MCP Tool | Expected Result | Verify By |
|------|--------|----------|-----------------|-----------|
| 0 | Confirm instance + create/set Update Set | SN-Get-Current-Instance, SN-Set-Update-Set | US current | SN-Get-Current-Update-Set |
| 1 | Create dictionary entry on incident | SN-Create-Record (sys_dictionary) | Field exists | SN-Explain-Field / SN-Query-Table sys_dictionary |
| 2 | Add field to incident form layout | SN-Create-Record (sys_ui_element) or BG script | Field visible on form | SN-Query-Table sys_ui_element |
| 3 | Create ACLs for field | SN-Batch-Create (sys_security_acl) | ACLs active | SN-Query-Table sys_security_acl |
| 4 | Inspect Update Set | SN-Inspect-Update-Set | 3+ components captured | Log output |

---

## 7. DO — Build Agent MUST

1. Replace placeholder `u_demo_custom_field` with user-confirmed API name before create
2. Use Update Set before any metadata change
3. Resolve no hardcoded sys_ids
4. Self-verify each step with SN-Query-Table
5. Log to `build/implementation-log.md` + evidence files

## 8. DO NOT — Build Agent MUST NOT

1. Create field with placeholder name without user confirmation
2. Modify OOB fields or task table dictionary globally
3. Skip ACLs on new field
4. Deploy to production via MCP
5. Assume Agent Workspace layout without checking handoff

---

## 9. Acceptance Criteria (for Test Agent)

| AC# | Criterion | Test Method | Pass Condition | Type |
|-----|-----------|-------------|----------------|------|
| AC1 | Field exists on incident table | SN-Explain-Field incident.u_* | Field returned with correct type | happy |
| AC2 | Field visible on form | Query sys_ui_element OR create incident and check via SN-Get-Incident | Element exists / value settable | happy |
| AC3 | itil can write field | SN-Create-Incident with field value → SN-Get-Incident | Value persisted | happy |
| AC4 | Field not on change_request | SN-Query-Table change_request | Column does not exist | regression |

---

## 10. Rollback Plan

| Artifact | Rollback |
|----------|----------|
| Dictionary + column | Deactivate/delete dictionary entry (careful in prod) |
| Form element | Delete sys_ui_element |
| ACLs | Deactivate ACL records |
| Full | Revert Update Set |

---

## 11. Deployment (human)

1. Complete Update Set in dev  
2. Migrate to test → verify AC1–AC4  
3. Prod: human approval required  

---

**Sign-off**: **DRAFT** — awaiting field name, type, and label from user. Design pattern is SN-compliant and ready for Build once confirmed.
