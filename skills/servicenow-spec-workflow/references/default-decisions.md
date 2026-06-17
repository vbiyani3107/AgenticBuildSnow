# Autonomous Default Decisions — Remote ServiceNow Development

When the user does **not** answer clarifying questions, agents **must not stall**. This enables remote development via chatbot without blocking on every gap.

**Protocol**: Ask once → if no answer within the same turn or user says *continue / proceed / build it*, apply defaults below → document every auto-decision in handoff **§3 Assumptions & Auto-Decisions** with `Source: DEFAULT`.

Only **HARD STOP** items block progress (see bottom). Everything else gets a best-practice default.

---

## Decision flow (Analysis Agent)

```
1. Batch clarifying questions (max 7, prioritized)
2. If user answers → use answers
3. If user silent, says "continue", invokes next agent, or pastes new instruction:
   → Apply defaults from this file
   → Mark handoff READY FOR DEVELOPMENT (with documented assumptions)
4. Never re-ask the same question in the same session unless user contradicts
```

Build, Test, Document agents: if handoff has `Source: DEFAULT` assumption and step is ambiguous, follow the assumption — do not re-ask user.

---

## Default decision matrix

| Question area | Default when unanswered | Rationale (ServiceNow practice) |
|---------------|-------------------------|----------------------------------|
| **Target instance** | MCP `SN-Get-Current-Instance` result | Remote dev uses configured dev/subprod connector |
| **Environment** | Development / sub-production | Never assume production |
| **Update Set** | Create new: `[JIRA-or-session-id] <short title>` | One US per story; SN SDLC standard |
| **Application scope** | Global for OOB ITSM tables; scoped app if requirement names a scoped app | Minimize cross-scope risk on OOB |
| **Module** | Incident Management if story mentions incident/P1/ticket; else infer from tables | Current team focus |
| **Roles affected** | `itil` + `sn_incident_read` for incident UI; `itil,change_manager` for change | Standard ITSM roles |
| **Test role** | `itil` (note MCP may run elevated — document in test report) | Test as practitioner not admin |
| **UI surface** | Both Agent Workspace and classic form if form change; else Agent Workspace first | SN direction toward Workspace |
| **Automation type (new)** | Flow Designer (`sys_hub_flow`) | SN recommendation over legacy Workflow |
| **Legacy Workflow** | Do not create new; extend only if requirement says "workflow" and discovery finds existing | Avoid new Workflow Editor artifacts |
| **Client Script vs UI Policy** | UI Policy + UI Policy Action first; Client Script only if UI Policy insufficient | Performance + maintainability |
| **Business Rule timing** | `after` + async for notifications/integrations; `before` for field validation | Avoid insert slowdown |
| **Business Rule table** | Most specific table (`incident` not `task`) | Regression prevention |
| **Notifications** | `sysevent_email_action` or Flow — not inline `GlideEmail` in BR | Maintainability |
| **Script Include** | Create when logic reused in 2+ scripts or >15 lines | DRY standard |
| **Hardcoded references** | Resolve by **name** via MCP query at build time; store in `sys_properties` if runtime lookup needed | Portability across instances |
| **Assignment** | Assignment Rule (`sysrule_assignment`) before BR assignment | OOB pattern first |
| **SLA impact** | No SLA change unless requirement mentions SLA | Avoid unintended SLA regression |
| **Data migration** | Out of scope; config-only in scope | Remote chatbot does one story config |
| **Domain separation** | Single domain `global` unless instance has domains and requirement mentions company | Confirm via query; default global |
| **PII / security** | Apply read restrictions via ACL + Data Policy on new sensitive fields | Secure by default |
| **Catalog / Portal** | Out of scope unless requirement mentions catalog, portal, or request | Narrow scope |
| **Dashboards / Reports** | Include only if requirement mentions analytics, dashboard, report | Avoid scope creep |
| **Scheduled jobs** | `sysauto_script` with clear name; prefer Flow scheduled trigger for new automation | Use platform-appropriate scheduler |
| **Update Set + MCP REST** | Create metadata in background script after `GlideUpdateSet.set()` in same script (see L001, L003) | REST-only create often skips `sys_update_xml` |
| **Fix scripts** | One-time data fix → Fix Script in Update Set, mark **execute manually post-deploy** in handoff | SN deployment practice |
| **Background script (MCP)** | Dev/test verification only — not production delivery mechanism | MCP is remote dev tool |
| **Acceptance criteria** | Analysis Agent derives minimum: 1 happy path + 1 negative + 1 regression | Testable SDLC |
| **Rollback** | Deactivate artifact or revert Update Set; document sys_ids | Standard rollback |
| **Jira key** | Use session_id slug if no Jira key provided | Traceability |

---

## Artifact selection defaults (requirement → artifact)

When requirement is vague, prefer this order:

| Need | 1st choice | 2nd choice | Avoid |
|------|------------|------------|-------|
| Field show/hide/mandatory | UI Policy | Client Script | Business Rule |
| Field value on save | Business Rule (before) | Data Policy | Client Script only |
| Cross-record automation | Flow Designer | Business Rule (async) | Synchronous BR chain |
| Email on event | Notification + Event | Flow | Script in BR |
| Reusable logic | Script Include | — | Copy-paste |
| One-time data correction | Fix Script | Background script (manual) | BR permanent hack |
| Recurring batch | Scheduled Job (`sysauto_script`) | Flow (scheduled) | Ad-hoc BR |
| Approval | Flow / Approval Policy | Workflow (existing only) | Custom BR approval |
| Integration outbound | Flow + REST step | MID Server script | Inline BR REST |
| Integration inbound | Scripted RESTART / REST API / Flow | — | Email parser unless specified |
| UI module/link | Application Menu + Module | — | Direct URL hardcode |
| Mobile | Agent Workspace layout / Mobile layout | Responsive classic | Desktop-only CS |
| Security | ACL → Data Policy → UI Policy | | Role check in script |

Full catalog: [platform-artifact-catalog.md](platform-artifact-catalog.md)

---

## MCP discovery defaults (Analysis / Build)

When instance data unknown:

1. `SN-Get-Current-Instance` — record in session.json
2. `SN-Discover-Table-Schema` / `SN-Get-Table-Schema` — before field changes
3. `SN-Query-Table` — resolve groups, users, choices by **name**
4. `SN-List-Update-Sets` — check for in-progress US before creating new
5. Log all discovery in `analyze/discovery-notes.md`

---

## HARD STOP — cannot default (must ask once; if still silent, mark BLOCKED with recommended default)

| Situation | Action |
|-----------|--------|
| Requirement explicitly says **production** | STOP — confirm once; if silent, proceed on **dev instance only** and document "prod deploy pending human approval" |
| **Delete** or deactivate OOB artifact | STOP — document risk; do not execute without explicit "yes delete" |
| Mutually exclusive requirements | STOP — pick safer option and document conflict |
| Legal/compliance constraint stated but undefined | Default secure (deny access) and document |
| User specifies wrong module (change vs incident) | Follow user literal text over default |

---

## Documentation requirement for every auto-decision

In handoff §3, each row must include:

| # | Decision | Selected value | Source | Risk if wrong |
|---|----------|----------------|--------|---------------|
| 1 | Target instance | dev12345 | DEFAULT | Low — MCP configured |

In chat summary, list: **"Auto-decisions applied (N)"** with bullet list so user can correct in rework.

---

## Other phases

| Phase | When user silent |
|-------|------------------|
| **Build** | Execute handoff including DEFAULT assumptions; mark BLOCKED only on MCP auth failure or HARD STOP |
| **Test** | Run all ACs; mark BLOCKED with manual UI steps if MCP cannot simulate role |
| **Document** | Produce full doc; flag assumptions and untested BLOCKED items prominently |
