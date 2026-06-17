---
name: sn-do
description: >-
  Natural-language entry for remote ServiceNow work via the pipeline orchestrator.
  Use when the user says pipeline orchestrator, sn-do, or casual SN requests: add,
  create, update, edit, modify, delete, remove fields, forms, rules, scripts,
  policies, flows on incident, change, or problem. Parses intent internally and
  runs Analyze → Build → Test → Document with smart defaults. Use for "try to
  add a field", "update the form", "delete that rule", or any conversational SN task.
---

# SN Do — Natural Language Pipeline Entry

**You are the conversational front door.** User talks normally → you parse intent → you run the **Pipeline Orchestrator** in **autonomous** mode (unless they say `strict` or `analyze only`).

Full orchestrator playbook: [sn-pipeline-orchestrator/SKILL.md](../sn-pipeline-orchestrator/SKILL.md)  
Intent mapping: [operation-intents.md](../servicenow-spec-workflow/references/operation-intents.md)

---

## What the user can say (no special format)

Examples that **all work**:

```
Hey pipeline orchestrator — add a new field on incident form, mandatory, classic.

Pipeline orchestrator try to update the assignment rule for network incidents.

/sn-do delete the test business rule from incident

Can you add a field to the incident form for external ticket ID?

With pipeline orchestrator — make u_demo_field mandatory on classic form.
```

User does **not** need: Jira key, API names, step lists, or `/sn-pipeline-orchestrator autonomous`.

---

## Step 1 — Parse (always, before anything else)

Extract and state briefly in chat:

| Slot | From user text | If missing |
|------|----------------|------------|
| **Intent** | CREATE / UPDATE / DELETE / ANALYZE_ONLY | Infer from verbs (add=CREATE) |
| **Entity** | incident, change, problem, catalog | Default: **incident** |
| **Object** | field, BR, UI policy, flow, ACL, … | Infer from nouns |
| **Modifiers** | mandatory, classic, optional, P1, etc. | Defaults per operation-intents.md |
| **Mode** | autonomous (default), strict, analyze_only | See trigger phrases |

Write parsed intent to user in 2–3 lines, then proceed **without waiting** unless HARD STOP (prod delete of OOB).

---

## Step 2 — Normalize requirement

Expand casual text into a clear one-paragraph requirement for `requirement/requirement.md`:

> **Intent**: CREATE  
> **Target**: incident form (classic)  
> **Ask**: Add new mandatory field [inferred label/name from context]  
> **Assumptions**: dev instance via MCP, new Update Set, ACLs for itil  

---

## Step 3 — Run pipeline orchestrator

Read and execute [sn-pipeline-orchestrator/SKILL.md](../sn-pipeline-orchestrator/SKILL.md) with:

| Setting | Value |
|---------|-------|
| **mode** | `autonomous` (unless user said strict) |
| **analyze_only** | true if user said don't build / just analyze |
| **requirement** | normalized paragraph from Step 2 |

Run all phases unless `analyze_only`.

---

## Step 4 — Tell user what happened

Short summary:

```
Parsed: CREATE field on incident (classic, mandatory)
Session: stories/<id>/
Assumed: u_external_ticket_id, string, itil ACLs (see handoff §3)
Result: SUCCESS | PARTIAL | ANALYSIS ONLY
Report: pipeline-execution-report.md
```

**If functional delivery complete on dev (L002)**: say explicitly *"You're done on dev — nothing required from you."* Migration notes belong in the report only.

If they only wanted analysis, say: *"Say 'continue build' or run `/sn-do` again without 'analyze only' to implement."*

---

## CRUD quick reference

| User says | You infer |
|-----------|-----------|
| add / create / new | CREATE |
| edit / update / change / modify / make X mandatory | UPDATE |
| delete / remove / drop | DELETE (deactivate preferred) |
| don't do it / just analyze | ANALYZE_ONLY, Phase 1 stop |

Details: [operation-intents.md](../servicenow-spec-workflow/references/operation-intents.md)

---

## DO

- Accept messy, short, conversational input
- Default to autonomous + incident + classic form for form fields
- Document every assumption in handoff §3
- Run full pipeline in one conversation when user wants action
- Use MCP `user-servicenow-demo` on dev instance for Build/Test

## DO NOT

- Require user to type skill names or templates
- Use strict mode unless user asks
- Hard-delete OOB artifacts without explicit confirmation
- Skip pipeline report when running full pipeline
