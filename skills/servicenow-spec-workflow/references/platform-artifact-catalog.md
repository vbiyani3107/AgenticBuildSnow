# ServiceNow Platform Artifact Catalog

Extensible reference for Analysis (design) and Build (implementation). When a story mentions any artifact type, use this catalog to pick the right table, pattern, and verification approach.

**Rule**: Prefer platform-native artifacts over custom script. Prefer configuration over code.

---

## Layer model

```
Presentation     → UI Policy, Client Script, Workspace Layout, Portal Widget
Business Logic   → Business Rule, Script Include, Flow, Workflow (legacy)
Data / Security  → Dictionary, ACL, Data Policy, Table Transform
Automation       → Flow, Scheduled Job, Event, Notification
Integration      → REST Message, Import Set, Transform Map, MID
Reporting        → Report, Dashboard, Performance Analytics
Deployment       → Update Set, Fix Script, Application Repository
```

---

## Configuration & data model

| Artifact | Table | When to use | Build via MCP | Verify |
|----------|-------|-------------|---------------|--------|
| Table | `sys_db_object` | New entity | SN-Create-Record / Batch | Schema query |
| Dictionary entry | `sys_dictionary` | New field on table | SN-Create-Record | SN-Explain-Field |
| Choice list | `sys_choice` | Controlled values | SN-Create-Record | Query choices |
| Reference qualifier | Dictionary or BR | Limit lookups | Config | Query reference |
| Table transform | `sys_transform_map` | Import mapping | SN-Create-Record | Run transform test |
| Number sequence | `sys_number` | Custom numbering | SN-Create-Record | Create record |

---

## Security & governance

| Artifact | Table | When to use | Notes |
|----------|-------|-------------|-------|
| ACL | `sys_security_acl` | Table/field/operation access | Deny by default; explicit allow |
| Data Policy | `sys_data_policy2` | Mandatory, read-only, encrypted on server | Server-enforced; prefer over CS for mandatory |
| UI Policy | `sys_ui_policy` | Show/hide, mandatory, read-only on form | Faster than Client Script |
| UI Policy Action | `sys_ui_policy_action` | Field actions for policy | REST limits — use background script if needed |
| Cross-scope privilege | Application ACL | Scoped app accessing OOB | Document in handoff |

---

## Client-side (form / UI)

| Artifact | Table | When to use | Prefer over |
|----------|-------|-------------|-------------|
| Client Script | `sys_script_client` | onLoad, onChange, onSubmit UI logic | — (last resort after UI Policy) |
| UI Action | `sys_ui_action` | Buttons, form links | |
| Formatter | `sys_ui_formatter` | Embedded HTML/widgets | |
| Declarative Form Action | Workspace | Agent Workspace behavior | Classic CS |
| Module | `sys_app_module` | Navigation link | Hardcoded URLs |
| Application Menu | `sys_app_application` | App menu container | |

**Client Script types**: `onLoad`, `onChange`, `onSubmit`, `onCellEdit` (lists)

---

## Server-side scripting

| Artifact | Table | When to use | Timing |
|----------|-------|-------------|--------|
| Business Rule | `sys_script` | Record lifecycle logic | before / after / async |
| Script Include | `sys_script_include` | Reusable server JS | Class or function |
| Fix Script | `sys_script_fix` | One-time deploy script | Manual run post-deploy |
| Scheduled Script | `sysauto_script` | Recurring batch | Cron / interval; **MCP**: BG script after `GlideUpdateSet.set()` (L003) |
| UI Script (legacy) | `sys_ui_script` | Shared client JS library | Include in CS |

**Business Rule filter**: Always set `filter condition` and correct `when` — never global unfiltered on `task`.

---

## Process automation

| Artifact | Table | When to use | Notes |
|----------|-------|-------------|-------|
| Flow Designer | `sys_hub_flow` | **New** automation, approvals, notifications | Preferred |
| Workflow (legacy) | `wf_workflow` | Extend existing only | Do not create new |
| Subflow | `sys_hub_flow` (subflow) | Reusable flow segments | |
| Approval Policy | `sysapproval_approver` / Flow | Multi-step approval | |
| Event | `sysevent_register` | Decouple BR from notification | BR fires event → notification |
| Notification | `sysevent_email_action` | Email templates | sys_id-free templates |

---

## ITSM — Incident (`incident` extends `task`)

Lifecycle: **New → In Progress → On Hold → Resolved → Closed** (+ Canceled)

| Need | Typical artifacts |
|------|-------------------|
| Auto-assign | Assignment Rule, BR (fallback) |
| Priority | BR on impact/urgency; OOB calculator |
| Resolve/Close validation | BR before, UI Policy |
| Major Incident | Plugin tables, dedicated flows |
| Child incidents | Related lists, BR |
| Email-to-incident | Inbound actions, flows |

Reference: [incident-management.md](incident-management.md)

---

## ITSM — Change (`change_request`)

Lifecycle: **New → Assess → Authorize → Scheduled → Implement → Review → Closed** (+ Canceled)

| State (typical) | Value |
|-----------------|-------|
| New | -5 |
| Assess | -4 |
| Authorize | -3 |
| Scheduled | -2 |
| Implement | -1 |
| Review | 0 |
| Closed | 3 |

| Need | Typical artifacts |
|------|-------------------|
| CAB approval | Flow, Approval |
| Risk assessment | BR, Client Script |
| Standard change template | `std_change_record_producer` |
| Collision detection | OOB + config |

Reference: [change-management.md](change-management.md)

---

## ITSM — Problem (`problem`)

Lifecycle: **New → Assess → Root Cause Analysis → Fix in Progress → Resolved → Closed**

| Need | Typical artifacts |
|------|-------------------|
| Link incidents | Related lists, BR |
| Known error | Knowledge + problem state |
| Root cause fields | UI Policy, mandatory on state |

Reference: [problem-management.md](problem-management.md)

---

## Service Catalog

| Artifact | Table | When |
|----------|-------|------|
| Catalog Item | `sc_cat_item` | Requestable service |
| Record Producer | `sc_cat_item` (producer) | Create task/incident from catalog |
| Variable | `item_option_new` | Form questions |
| Catalog UI Policy | `catalog_ui_policy` | Show/hide variables |
| Catalog Client Script | `catalog_script_client` | Variable logic |
| Workflow/Flow on order | Flow on `sc_req_item` | Fulfillment |

MCP: `SN-Catalog-*`, `SN-Validate-Configuration`

---

## Reporting & visibility

| Artifact | Table | When |
|----------|-------|------|
| Report | `sys_report` | Tabular/chart/list |
| Dashboard | `sys_dashboard` | Multi-report view |
| Homepage | `sys_home` | Role landing |

MCP demo tools exist for dashboards/reports — use only when requirement specifies.

---

## Integration

| Artifact | Table | When |
|----------|-------|------|
| REST Message | `sys_rest_message` | Outbound REST |
| Scripted REST API | `sys_ws_definition` | Inbound API |
| Import Set | `sys_import_set` | Staged load |
| Transform Map | `sys_transform_map` | Import to target |
| MID Server | `ecc_agent` | On-prem integration |

---

## Remote development via MCP — pattern by artifact

| Artifact type | Primary MCP approach |
|---------------|---------------------|
| Simple config record | SN-Create-Record / SN-Update-Record |
| Multi-record setup | SN-Batch-Create (transactional) |
| Update Set current | SN-Set-Update-Set + SN-Execute-Background-Script |
| REST-blocked fields | SN-Execute-Background-Script with setValue |
| Verification | SN-Query-Table, SN-Get-Record, SN-Inspect-Update-Set |
| Incident test | SN-Create-Incident, SN-Assign-Incident, etc. |
| Change test | SN-List-ChangeRequests, SN-Assign-Change, etc. |
| One-time fix | SN-Create-Fix-Script or fix script record |

---

## Classification keywords (Analysis Agent)

Map requirement language → artifact:

| Keywords | Likely artifacts |
|----------|------------------|
| show, hide, mandatory, read-only | UI Policy, Data Policy |
| validate, before save | BR (before), Client Script onSubmit |
| when created, when updated | BR, Flow trigger |
| email, notify, escalation | Notification, Flow |
| every night, daily, schedule | Scheduled Job, Flow schedule |
| button, click | UI Action |
| menu, module, navigate | Module |
| dashboard, report, KPI | Report, Dashboard |
| API, REST, integrate | REST Message, Scripted REST |
| import, CSV, load data | Import Set, Transform |
| approval, CAB, authorize | Flow approval |
| catalog, order, request | Catalog item, Flow |
| mobile, agent workspace | Workspace layout, Declarative actions |
| fix data once | Fix Script |
| reusable function | Script Include |

---

## Extensibility

New artifact type not listed:

1. Add row to this catalog (Analysis discovery-notes)
2. Document table name, MCP approach, verification query
3. Add module reference if domain-specific
4. Do not invent — confirm table via `SN-List-Available-Tables`
