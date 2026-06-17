# ServiceNow Remote Development — Reference Index

All skills live in `~/.cursor/skills/`. This index is the map.

## Agents (invoke in Cursor)

| Skill | How to call | SDLC phase |
|-------|-------------|------------|
| **SN Do (start here)** | Say *"pipeline orchestrator …"* or `/sn-do …` | **Full pipeline, natural language** |
| Analysis | `/sn-analysis-agent` | Intake + Design |
| Build | `/sn-development-agent` | Build |
| Test | `/sn-testing-agent` | QA |
| Document | `/sn-documentation-agent` | Documentation |
| **Pipeline** | `/sn-pipeline-orchestrator` | Engine (usually via sn-do) |

## Natural language (recommended)

```
Pipeline orchestrator — add a mandatory field on incident classic form.

/sn-do update the assignment rule for P1 network incidents.

Pipeline orchestrator remove the test field from incident form. Just analyze.
```

Skill: `sn-do` auto-loads in mcpdemo via `.cursor/rules/servicenow-remote-dev.mdc`

Intent mapping: `references/operation-intents.md`

Orchestrator: `/servicenow-spec-workflow` (overview)

## Reference library

| File | Content |
|------|---------|
| `servicenow-spec-workflow/references/session-protocol.md` | One session = one folder |
| `servicenow-spec-workflow/references/default-decisions.md` | **When user doesn't answer** |
| `servicenow-spec-workflow/references/platform-artifact-catalog.md` | **All SN artifact types** |
| `servicenow-spec-workflow/references/sdlc-remote-development.md` | SDLC + walkthrough examples |
| `servicenow-spec-workflow/references/servicenow-best-practices.md` | Dev standards |
| `servicenow-spec-workflow/references/incident-management.md` | Incident lifecycle |
| `servicenow-spec-workflow/references/change-management.md` | Change lifecycle |
| `servicenow-spec-workflow/references/problem-management.md` | Problem lifecycle |
| `servicenow-spec-workflow/references/self-learning-protocol.md` | **Self-learning capture + promotion** |
| `servicenow-spec-workflow/references/learnings-registry.md` | **Promoted learnings (read every session)** |

## Platform breadth covered

UI Policies, UI Policy Actions, Data Policies, Client Scripts, Business Rules, Script Includes, Fix Scripts, Scheduled Jobs (`sysauto_script`), Background scripts (MCP verify), Flow Designer, Notifications, Events, ACLs, Dictionary/fields, Assignment Rules, Modules, Catalog items, Workflows (extend only), Reports/Dashboards (when required), REST/integration patterns.

## Autonomous remote dev flow

```
New chat → paste requirement → /sn-analysis-agent
  → (questions once → defaults if silent)
  → handoff READY
→ /sn-development-agent → MCP on dev instance
→ /sn-testing-agent → evidence per AC
→ /sn-documentation-agent → Jira + deploy runbook
→ Human: migrate Update Set to prod
```

## Session artifacts location

`.cursor/servicenow-sessions/<session_id>/` in workspace.

See `INDEX.md` in that folder for all sessions.
