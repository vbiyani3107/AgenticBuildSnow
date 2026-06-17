# ServiceNow Development Best Practices

Reference for all SN spec-workflow agents. Apply unless handoff overrides with documented reason.

**Related**: [platform-artifact-catalog.md](platform-artifact-catalog.md) | [default-decisions.md](default-decisions.md) | [sdlc-remote-development.md](sdlc-remote-development.md)

---

## SDLC & deployment

| Rule | Detail |
|------|--------|
| One Update Set per story | Name: `[JIRA-KEY] Short description` |
| Set current before changes | `SN-Set-Update-Set` + `SN-Execute-Background-Script` |
| Inspect before complete | `SN-Inspect-Update-Set` — components + dependencies |
| Scoped application | Set scope before scoped artifacts; avoid global edits in scoped app |
| Dev → Test → Prod | Never skip test env; remote MCP = dev/subprod only by default |
| Fix Scripts | One-time; document manual execution in deployment notes |
| Version control | Update Set = migration unit; optional Git via SN Git Integration if instance has it |

---

## Artifact selection hierarchy

```
1. Configuration (UI Policy, Assignment Rule, Data Policy, Flow)
2. Script Include + thin Business Rule
3. Business Rule / Client Script (specific, filtered)
4. Fix Script (one-time only)
```

Never jump to Client Script when UI Policy suffices. Never create new Workflow when Flow Designer fits.

---

## Naming conventions

| Artifact | Pattern | Example |
|----------|---------|---------|
| Business Rule | `[Module] Purpose (table)` | `[INC] Validate resolve fields (incident)` |
| Script Include | `PascalCase` | `IncidentResolveValidator` |
| Client Script | `[UI] Purpose (table)` | `[INC] Warn on close without CI` |
| UI Policy | `[Module] Condition → action` | `[INC] Show cause when Resolved` |
| Data Policy | `[Module] Mandatory field policy` | |
| Flow | `[Module] Trigger - action` | `[INC] P1 - notify duty manager` |
| Scheduled Job | `[Module] Batch description` | `[INC] Nightly stale ticket review` |
| Update Set | `[JIRA-123] Description` | |
| Fix Script | `[JIRA-123] One-time purpose` | |
| ACL | `[table].[field] for [role]` | |

---

## Business Rules

| Practice | Detail |
|----------|--------|
| Table | Most specific (`incident` not `task`) |
| When | `before` validation; `after` side effects; `async` notifications/integrations |
| Filter condition | Always — never unfiltered on parent tables |
| setWorkflow(false) | Only when handoff requires; document why |
| GlideRecord | `addQuery`, `setLimit(1)` for lookups; avoid dot-walking in hot paths |
| Events | Fire event from BR; Notification listens to event |
| Order | Note execution order if multiple BRs on same table/when |

---

## Client Scripts & UI Policies

| Practice | Detail |
|----------|--------|
| Prefer UI Policy | Show/hide, mandatory, read-only |
| Client Script | onChange/onSubmit when UI Policy cannot |
| GlideUser / g_form | Standard APIs; no DOM hacking unless necessary |
| Performance | Avoid server calls in onChange loops |
| Agent Workspace | Check if Declarative Form Action applies |

---

## Data Policies

| Practice | Detail |
|----------|--------|
| Use for | Server-side mandatory, read-only, encrypted fields |
| Align | UI mandatory + Data Policy for same field |
| PII | Mask + encrypt sensitive fields |

---

## Script Includes

| Practice | Detail |
|----------|--------|
| Create when | Logic reused 2+ times or >15 lines |
| API | `Class.create()` for OOP; function includes for utilities |
| Client callable | Only when needed; mark `client callable` carefully |

---

## Flow Designer

| Practice | Detail |
|----------|--------|
| New automation | Default choice |
| Error handling | Flow error handling / rollback activities |
| Subflows | Reusable segments |
| Trigger | Record created/updated conditions explicit |

---

## Scheduled jobs & background

| Artifact | When |
|----------|------|
| `sysauto_script` | Recurring batch maintenance |
| Flow schedule | Business automation on timer |
| Fix Script | **Once** — not recurring |
| MCP background script | Dev verification only — not production delivery |

**Read-only job verification (L005)**: compare `sys_updated_on` before/after script run — no manual user check required.

---

## Security & governance

- **ACLs**: Every new table/field; deny implicit; explicit allow for roles
- **Least privilege**: No `admin` checks in scripts; use roles from handoff
- **Cross-scope**: Document elevated privileges in handoff
- **Input sanitization**: No `eval()`; escape user input in Jelly/scripts
- **No hardcoding**: sys_ids, groups, users — resolve by name or sys_properties
- **Audit**: Work notes / journal for user-visible changes; `gs.info` for system

---

## Data integrity

- Table hierarchy: `task` → `incident` / `change_request` / `problem`
- Choice lists over free text
- Reference fields with qualifiers
- Domain separation: `sys_domain` on queries when multi-domain
- Avoid duplicate records: check existence before create in Fix Scripts

---

## UI / modules / dashboards

- **Modules**: Application Menu → Module; roles on module
- **Dashboards**: Role-specific; avoid personal dashboards for team features
- **Reports**: Use database view only when report cannot query directly
- **Mobile / Workspace**: Test layout if form changed

---

## Performance

- BR: filter + async for heavy work
- Index custom fields used in queries
- Cache with `GlideCache` / properties for static lookups
- Bulk operations: batch with limit in Fix Scripts

---

## Documentation in instance

Every artifact:
- **Name**: follows convention
- **Short description**: one line
- **Description**: Jira ref, purpose, author, date
- **Script comments**: why, not what

---

## Verification (all agents)

1. Record/artifact exists with expected values
2. In current Update Set (metadata)
3. Works for target role (document MCP elevation if admin-only)
4. No regression on related tables in handoff
5. Evidence file or query logged in session folder

---

## Remote development specifics

- Autonomous defaults: [default-decisions.md](default-decisions.md)
- Resolve references by name via MCP at build time
- Document all sys_ids in implementation log after creation
- Never assume prod — document human promotion steps in Jira doc
