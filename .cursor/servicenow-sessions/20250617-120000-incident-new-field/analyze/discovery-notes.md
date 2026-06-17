# Discovery Notes — Analysis Phase

**Session**: 20250617-120000-incident-new-field  
**Date**: 2026-06-17

## Instance (MCP)

| Field | Value |
|-------|-------|
| Name | accenture-demo |
| URL | https://accentureservicessrodemo4.service-now.com |
| Verified | SN-Get-Current-Instance |

## Table: incident

- **Label**: Incident
- **Extends**: task (via super_class)
- **Existing custom fields observed** (u_* prefix): `u_ai_involvement`, `u_troubleshoot_steps`, `u_user_impacted`, `u_analysis`, `u_person_id`, etc.
- **Convention on this instance**: custom fields use `u_` prefix

## Form surfaces to consider

| Surface | Notes |
|---------|-------|
| Classic incident form | sys_ui_section / form layout |
| Agent Workspace | may need separate layout (UX Form / AWA) |
| Mobile | optional |

## Existing similar fields

| Field | Type | Relevance |
|-------|------|-----------|
| u_troubleshoot_steps | string(1000) | text field example on incident |
| u_user_impacted | integer | numeric custom field example |
| cause | string(4000) | OOB "Probable cause" — avoid duplicate purpose |

## Query not run (analysis only)

- Update Set list — deferred to Build phase
- Form view/layout records — Build should query `sys_ui_section`, `sys_ui_element` for incident form
