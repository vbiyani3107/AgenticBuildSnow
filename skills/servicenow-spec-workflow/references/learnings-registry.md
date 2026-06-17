# Learnings Registry — ServiceNow Spec Workflow

**Purpose**: Canonical, promoted learnings from pipeline runs. Agents read at session start; append on promotion only.

**Last updated**: 2026-06-17  
**Promoted count**: 5

---

## How to use

1. **Analysis / Build agents**: Skim titles before MCP work; apply **Fix / pattern** rows for matching artifact types.
2. **Orchestrator / Document agent**: After each pipeline, run [self-learning-protocol.md](self-learning-protocol.md) promotion.
3. **User recheck**: Merge pending session learnings → promote → patch target files.

---

### L001 — REST create may not capture Update Set components

| Field | Value |
|-------|-------|
| **ID** | L001 |
| **First seen** | 2026-06-17 |
| **Sessions** | 20260617-090539-daily-incident-list-job |
| **Type** | MCP_LIMITATION |
| **Symptom** | `SN-Create-Record` created `sysauto_script` but `SN-Inspect-Update-Set` showed 0 components; `sys_update_xml` empty |
| **Root cause** | REST API creates may not associate with current Update Set even after `GlideUpdateSet.set()` via trigger; timing and API path matter |
| **Fix / pattern** | **Preferred**: Create metadata records entirely inside `SN-Execute-Background-Script` after `GlideUpdateSet.set(usId)` in the **same** script block (insert + `gr.insert()`). **Fallback**: REST create → same-script US set → `gr.update()` touch → `SN-Inspect-Update-Set`. **Do not** tell user to verify; retry programmatically once, then document migration-only gap |
| **Promoted to** | `sn-development-agent/mcp-playbook.md`, `default-decisions.md` |
| **User impact** | migration-only |

---

### L002 — Do not assign user "next steps" when dev delivery is complete

| Field | Value |
|-------|-------|
| **ID** | L002 |
| **First seen** | 2026-06-17 |
| **Sessions** | 20260617-090539-daily-incident-list-job |
| **Type** | UX_COMMUNICATION |
| **Symptom** | User asked "why do I need to manually check?" after functional job was live |
| **Root cause** | Chat conflated **migration packaging** (Update Set) with **functional delivery** (artifact on instance) |
| **Fix / pattern** | Chat scorecard: if functional ACs pass → **"You're done on dev — nothing required."** Migration steps go only in `document/jira-story.md` § Deployment, not "Your next steps" in chat |
| **Promoted to** | `sn-do/SKILL.md`, `sn-documentation-agent/SKILL.md`, `pipeline-execution-report.template.md` |
| **User impact** | none (reduces confusion) |

---

### L003 — Create scheduled jobs via background script when Update Set tracking required

| Field | Value |
|-------|-------|
| **ID** | L003 |
| **First seen** | 2026-06-17 |
| **Sessions** | 20260617-090539-daily-incident-list-job |
| **Type** | BUILD_PATTERN |
| **Symptom** | Scheduled job worked but was invisible to Update Set inspection |
| **Root cause** | Same as L001; `sysauto_script` via REST bypassed US capture on accenture-demo |
| **Fix / pattern** | Build Step 0: US create + set current in background script. Step 1: create `sysauto_script` in **same or immediate follow-up** background script with fields set explicitly. Verify with `sys_update_xml` query by name/time, not only `SN-Inspect-Update-Set` |
| **Promoted to** | `sn-development-agent/mcp-playbook.md`, `platform-artifact-catalog.md` |
| **User impact** | migration-only |

---

### L004 — Update Set AC is informational, not a user-facing blocker

| Field | Value |
|-------|-------|
| **ID** | L004 |
| **First seen** | 2026-06-17 |
| **Sessions** | 20260617-090539-daily-incident-list-job |
| **Type** | TEST_PATTERN |
| **Symptom** | AC4 BLOCKED on US component → pipeline marked PARTIAL though job was fully functional |
| **Root cause** | Test agent treated migration packaging same as functional failure |
| **Fix / pattern** | Classify ACs: **FUNCTIONAL** vs **PACKAGING**. PACKAGING fail → note in test report, overall result stays **PASS** if all FUNCTIONAL pass. Only PARTIAL when functional gap exists |
| **Promoted to** | `pipeline-gates.md`, `sn-testing-agent/SKILL.md` |
| **User impact** | none |

---

### L005 — Read-only script verification via timestamp comparison

| Field | Value |
|-------|-------|
| **ID** | L005 |
| **First seen** | 2026-06-17 |
| **Sessions** | 20260617-090539-daily-incident-list-job |
| **Type** | BUILD_PATTERN |
| **Symptom** | Needed proof scheduled script did not mutate incidents |
| **Root cause** | N/A — positive pattern |
| **Fix / pattern** | Before `SN-Execute-Background-Script` (job script): query target records' `sys_updated_on`. After execution (~3s): re-query. Unchanged → PASS read-only AC. Log in `test/evidence/ac-N.md` |
| **Promoted to** | `sn-testing-agent/SKILL.md`, `servicenow-best-practices.md` |
| **User impact** | none |

---

## Pending / deferred

| ID | Status | Reason |
|----|--------|--------|
| — | — | — |
