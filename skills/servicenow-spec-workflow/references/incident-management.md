# Incident Management Module Reference

Default module for spec-workflow agents. Load when stories touch incidents, tickets, major incidents, or ITSM service desk.

**Also see**: [platform-artifact-catalog.md](platform-artifact-catalog.md) | [change-management.md](change-management.md) | [problem-management.md](problem-management.md)

---

## Core tables

| Table | Purpose |
|-------|---------|
| `incident` | Primary records (extends `task`) |
| `incident_task` | Child tasks |
| `task_sla` / `contract_sla` | SLA definitions and task SLAs |
| `sysrule_assignment` | Assignment rules |
| `sys_email` | Email audit |
| `sys_attachment` | Attachments |
| `problem` | Linked via `problem_id` |

**Key fields**: `number`, `short_description`, `description`, `caller_id`, `contact_type`, `category`, `subcategory`, `priority`, `urgency`, `impact`, `state`, `assignment_group`, `assigned_to`, `opened_by`, `resolved_at`, `closed_at`, `close_code`, `close_notes`, `business_service`, `cmdb_ci`, `company`, `location`, `problem_id`, `parent_incident`, `child_incidents`.

---

## Lifecycle

```
                    ┌──────────┐
         create ──► │   New    │ (1)
                    └────┬─────┘
                         │ assign / work
                    ┌────▼─────┐
              ┌────►│In Progress│ (2)◄────┐
              │     └────┬─────┘         │
              │          │               │
         ┌────▼────┐     │          ┌────┴────┐
         │ On Hold │ (3) │          │ reopen  │
         └────┬────┘     │          └─────────┘
              │          │
              │     ┌────▼─────┐
              │     │ Resolved │ (6)
              │     └────┬─────┘
              │          │ close
              │     ┌────▼─────┐
              └─────┤  Closed  │ (7)
                    └──────────┘
              
         Canceled (8) — from New/In Progress in some processes
```

**Always** confirm state values on target instance (`SN-Explain-Field` on `incident.state`).

### State transition rules (typical)

| From | To | Common requirements |
|------|-----|---------------------|
| New | In Progress | Assignment optional |
| In Progress | On Hold | Hold reason (custom field) |
| In Progress | Resolved | Resolution code, notes |
| Resolved | Closed | Auto-close after timer or manual |
| Resolved | In Progress | Reopen — preserve history |
| * | Canceled | Authorization / state guard |

Encode required fields per transition in handoff when story affects resolve/close.

---

## Priority

Priority = f(impact, urgency) on most instances. **Do not** override with BR unless requirement says so — check OOB `Priority` calculation first.

| Priority | Label (typical) |
|----------|-----------------|
| 1 | Critical |
| 2 | High |
| 3 | Moderate |
| 4 | Low |
| 5 | Planning |

---

## Artifact mapping (incident stories)

| Need | 1st choice | Table |
|------|------------|-------|
| Auto-assign | Assignment Rule | `sysrule_assignment` |
| Field validation on save | BR (before) + Data Policy | `sys_script`, `sys_data_policy2` |
| Form show/hide | UI Policy | `sys_ui_policy` |
| onChange UX | Client Script | `sys_script_client` |
| Email on assign/resolve | Event + Notification or Flow | `sysevent_*`, `sys_hub_flow` |
| SLA change | SLA Definition / Task SLA | `contract_sla` |
| Self-service create | Record Producer / Catalog | `sc_cat_item` |
| Major incident | Plugin + dedicated process | varies |
| Link to problem | Related list / BR | `problem` |
| Attach CI | Reference + optional BR | `cmdb_ci` |

---

## Form & UI surfaces

| Surface | Consider when |
|---------|---------------|
| Classic incident form | Legacy ITSM users |
| Agent Workspace | Primary for agents (default) |
| Service Portal | Caller-facing create/view |
| Mobile | Field simplification |

Default if user silent: configure for **Agent Workspace + classic** when changing form behavior.

---

## Analysis checklist

- [ ] Roles: `itil`, `sn_incident_read`, `sn_incident_write`, caller?
- [ ] Caller vs opened_by vs assigned_to
- [ ] SLA impact (pause on hold, stop on resolve)
- [ ] Major Incident / Outage plugins
- [ ] Email inbound (create) / outbound (notify)
- [ ] Child/parent incidents
- [ ] CMDB CI mandatory rules
- [ ] Domain separation
- [ ] Integration (monitoring tool → incident)
- [ ] Knowledge link on resolve

---

## Testing matrix (minimum)

| # | Scenario | Type |
|---|----------|------|
| T1 | Create incident — happy path | Functional |
| T2 | Update / assign / reassign | Functional |
| T3 | Resolve with mandatory fields | Functional |
| T4 | Close from resolved | Functional |
| T5 | Negative — should NOT trigger | Regression |
| T6 | Edge case from requirement | Boundary |
| T7 | Related task type unaffected | Regression (`change_request` unchanged) |

---

## MCP tools

| Tool | Use |
|------|-----|
| `SN-List-Incidents` / `SN-Get-Incident` | Read |
| `SN-Create-Incident` | Create test records |
| `SN-Assign-Incident` | Assignment |
| `SN-Resolve-Incident` / `SN-Close-Incident` | Lifecycle |
| `SN-Add-Work-Notes` / `SN-Add-Comment` | Journal |
| `SN-Query-Table` | Flexible validation |

Prefix test data: `[TEST-<session_id>]` in short_description.

---

## Anti-patterns

- BR on `task` when only incident in scope
- Close without resolve (breaks SLA metrics)
- Overlapping assignment rules (same order, conflicting conditions)
- Client Script duplicating server validation inconsistently
- Inline email in BR instead of Notification/Flow
- Hardcoded group/user sys_ids
- Synchronous BR chain on high-volume insert
