# Operation Intents — Natural Language → ServiceNow Pipeline

When the user speaks casually ("add a field", "update the form", "delete that rule"), map their words to an **operation intent** before Analysis designs the handoff.

**Default mode**: `autonomous` — apply [default-decisions.md](default-decisions.md) for gaps; document in handoff §3.

---

## Trigger phrases (auto-start pipeline)

Any of these mean **run the full pipeline** (or analysis-only if user says so):

| User says | Action |
|-----------|--------|
| "pipeline orchestrator …" | Run orchestrator |
| "with pipeline orchestrator try to …" | Run orchestrator |
| "/sn-do …" | Run orchestrator |
| "on ServiceNow …" / "in incident form …" | Run orchestrator if SN context |
| "add / create / new …" | CREATE intent |
| "edit / update / change / modify …" | UPDATE intent |
| "delete / remove / deactivate …" | DELETE intent |
| "just analyze" / "don't do it" / "don't build" | ANALYZE_ONLY — stop after Phase 1 |

No need for `/sn-pipeline-orchestrator autonomous` — that is the default when using natural language entry.

---

## CRUD intent mapping

| Intent | User keywords | SN meaning | Typical artifacts |
|--------|---------------|------------|-------------------|
| **CREATE** | add, create, new, introduce, build | New metadata or config | Dictionary, UI Policy, BR, Flow, ACL, Module |
| **UPDATE** | edit, update, change, modify, set, make mandatory | Change existing artifact/field | sys_dictionary update, UI Policy, deactivate+recreate |
| **DELETE** | delete, remove, deactivate, drop | Retire config (prefer deactivate) | Set active=false; document rollback |
| **READ/TEST** | check, verify, test, validate | Test phase emphasis | Query via MCP; may skip build if nothing to change |

### CREATE examples

| User request | Inferred design |
|--------------|-----------------|
| "add a field to incident form" | Dictionary on `incident` + form element + ACLs |
| "add mandatory field classic form" | + Data Policy mandatory; classic `sys_ui_element` |
| "create assignment rule for P1" | `sysrule_assignment` on incident |
| "add notification when assigned" | Event + `sysevent_email_action` or Flow |

### UPDATE examples

| User request | Inferred design |
|--------------|-----------------|
| "make field mandatory" | Data Policy and/or UI Policy; align client/server |
| "change label of field X" | Update `sys_dictionary` column label |
| "update BR to run async" | UPDATE `sys_script` when field |
| "edit form to show field when resolved" | UI Policy condition state=6 |

### DELETE examples

| User request | Inferred design |
|--------------|-----------------|
| "remove field from form" | Remove `sys_ui_element` (column may remain) |
| "delete custom field" | Deactivate dictionary; **confirm** if user said delete |
| "remove business rule X" | Deactivate `sys_script`; verify no dependency |

**DELETE guardrail**: Prefer **deactivate** over hard delete. If user said "delete" without naming artifact → Analysis proposes target from discovery; Build requires handoff entry.

---

## Entity detection (what table/module)

| User mentions | Default table/module |
|---------------|---------------------|
| incident, ticket, INC | `incident` / incident-management |
| change, CHG | `change_request` / change-management |
| problem, PRB | `problem` / problem-management |
| form (no table) | **incident** (team default) |
| catalog, request item | Service Catalog |
| UI, policy, script (no table) | Resolve from discovery or ask **one** question |

---

## Field CREATE defaults (when user is vague)

When user says "add a field" without details:

| Attribute | Default | Source |
|-----------|---------|--------|
| Table | incident | DEFAULT |
| API name | `u_` + slug from label/purpose (max 30 chars) | DEFAULT |
| Label | Title Case from purpose words | DEFAULT |
| Type | string(255) | DEFAULT |
| Mandatory | optional unless user said mandatory/required | USER or DEFAULT |
| Form | classic incident form | DEFAULT |
| ACL | read/write itil | DEFAULT |
| Update Set | new `[session-id] description` | DEFAULT |

If user says **"mandatory"** → Data Policy mandatory + UI Policy mandatory on classic form.

If user says **"choice"** or lists values → type = choice + `sys_choice` records.

---

## Pipeline modes from natural language

| User signal | Mode | Pipeline depth |
|-------------|------|----------------|
| (none) | autonomous | Analyze → Build → Test → Document |
| "strict" / "no assumptions" | strict | Stop on BLOCKING gaps |
| "analyze only" / "don't do it" | autonomous + **analyze_only** | Phase 1 only |
| "build but don't test" | autonomous + stop after build | Rare; document in report |

---

## One-turn flow (what agent does internally)

```
1. Parse: intent (CREATE/UPDATE/DELETE) + entity (incident/…) + modifiers (mandatory, classic)
2. Normalize to one-line requirement → requirement/requirement.md
3. Bootstrap session folder
4. Run Analysis with defaults → handoff READY (autonomous)
5. Unless analyze_only:
   Run Build → Test → Document
6. Write pipeline-execution-report.md + chat scorecard
7. Tell user: session path + what was assumed (§3 bullets)
```

User sees one message in, full pipeline out.

---

## Example invocations (copy-paste)

**Vague CREATE (works):**
```
Hey pipeline orchestrator — add a new field on the incident form, make it mandatory, classic form.
```

**UPDATE:**
```
Pipeline orchestrator: update the incident form so u_external_ticket_id is mandatory on resolve.
```

**DELETE:**
```
Pipeline orchestrator: remove the demo custom field from the incident form.
```

**Analyze only:**
```
Pipeline orchestrator — add a field to incident form. Just analyze, don't build yet.
```

**Short alias:**
```
/sn-do add mandatory field to incident classic form for external reference number
```
