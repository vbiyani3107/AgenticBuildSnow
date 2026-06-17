# Self-Learning Protocol — ServiceNow Spec Workflow

The workflow **learns from every pipeline run**. Mistakes, MCP limitations, user confusion, and patterns that worked are captured, promoted into shared references, and applied on the **next** run automatically.

**Registry**: [learnings-registry.md](learnings-registry.md) (canonical, append-only promoted learnings)

---

## When to capture (every agent)

| Trigger | Example | Capture where |
|---------|---------|---------------|
| MCP tool behaved unexpectedly | REST create skipped `sys_update_xml` | `session/learnings.md` |
| User asked "why manual?" | Over-emphasized US step when job was live | `session/learnings.md` |
| Rework fixed a gap | Background script before REST create worked | `session/learnings.md` |
| Pattern worked well | Read-only verify via before/after timestamps | `session/learnings.md` |
| Test BLOCKED for env limitation | Role simulation impossible via MCP | `session/learnings.md` |

**Rule**: If it would help the *next* story, write it down — even if the current story still succeeded.

---

## Session capture file

Each pipeline run SHOULD have:

```
stories/<session_id>/learnings.md
```

Use [templates/learnings-session.template.md](../templates/learnings-session.template.md).

Minimum at pipeline end: **1 row** if anything non-trivial happened (including "no new learnings").

---

## Promotion algorithm (orchestrator + documentation agent)

Run at **end of Phase 4 (Document)** or when user asks to recheck skills:

```
1. Read session/learnings.md (if missing, harvest from test-report + implementation-log + chat)
2. For each entry with status PROPOSED:
   a. Dedupe against learnings-registry.md (same root cause → merge, bump session count)
   b. Classify: MCP_LIMITATION | UX_COMMUNICATION | BUILD_PATTERN | TEST_PATTERN | GATE_POLICY
   c. If confidence HIGH or seen in 2+ sessions → PROMOTE
3. PROMOTE = append to learnings-registry.md + patch target reference files (see table below)
4. Set session learning status → PROMOTED or DEFERRED (with reason)
5. Update learnings-registry.md `last_updated` and `promoted_count`
```

### Promotion targets

| Classification | Patch these files |
|----------------|-------------------|
| MCP_LIMITATION | `sn-development-agent/mcp-playbook.md`, `platform-artifact-catalog.md` |
| BUILD_PATTERN | `mcp-playbook.md`, `servicenow-best-practices.md`, `default-decisions.md` |
| TEST_PATTERN | `pipeline-gates.md`, `sn-testing-agent/SKILL.md`, test-report template |
| UX_COMMUNICATION | `sn-do/SKILL.md`, `sn-documentation-agent/SKILL.md`, `pipeline-execution-report.template.md` |
| GATE_POLICY | `pipeline-gates.md`, `sn-pipeline-orchestrator/SKILL.md` |

**Agents MUST read `learnings-registry.md` at session start** (analysis + build at minimum).

---

## Learning entry schema (registry)

```markdown
### LNNN — Short title

| Field | Value |
|-------|-------|
| **ID** | LNNN |
| **First seen** | YYYY-MM-DD |
| **Sessions** | session-id-1, session-id-2 |
| **Type** | MCP_LIMITATION \| UX_COMMUNICATION \| BUILD_PATTERN \| TEST_PATTERN \| GATE_POLICY |
| **Symptom** | What went wrong or surprised us |
| **Root cause** | Why |
| **Fix / pattern** | What to do next time |
| **Promoted to** | list of file paths |
| **User impact** | none \| migration-only \| blocking |
```

---

## Delivery vs migration (critical UX learning)

| Question | If YES → tell user | If NO → do NOT ask user to |
|----------|-------------------|---------------------------|
| Is the artifact live and functional on dev? | "Done — nothing required" | Open UI to verify |
| Is Update Set empty but artifact exists? | Note in deploy runbook only | "Your next steps" in chat |
| Did functional ACs pass? | SUCCESS / PARTIAL (migration) | Imply homework for dev use |

**Pipeline result**:
- **SUCCESS** — all in-scope functional ACs pass; migration packaging gaps are documented, not user blockers
- **PARTIAL** — functional gap OR user-requested scope incomplete
- **FAILED** — build/test could not deliver core requirement

---

## Mandatory orchestrator step: Learning harvest

After G4 passes, before final chat scorecard:

1. Write/update `session/learnings.md`
2. Run promotion algorithm
3. Add row to `pipeline-execution-report.md` § **Learnings promoted**
4. If new HIGH-confidence learning → patch registry + target files in same run

---

## Self-recheck command

When user says *"recheck skills"*, *"self learning"*, *"update workflow from mistakes"*:

1. Scan recent sessions: `stories/*/learnings.md`, `test-report.md`, `implementation-log.md`
2. Promote any unpromoted PROPOSED entries
3. Reconcile registry vs agent skills (orchestrator, mcp-playbook, gates) — patch gaps
4. Report: learnings promoted, files patched, nothing pending

---

## DO

- Capture learnings in the same conversation when discovered
- Promote durable patterns to shared refs immediately when confidence HIGH
- Read registry at analysis/build start
- Distinguish dev delivery complete vs migration packaging

## DO NOT

- Ask user to manually verify when MCP already proved functional delivery
- Leave learnings only in chat (must hit disk)
- Promote session-specific sys_ids (patterns only)
- Duplicate registry entries — merge instead
