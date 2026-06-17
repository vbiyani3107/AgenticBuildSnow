---
name: sn-pipeline-orchestrator
description: >-
  ServiceNow Pipeline Orchestrator engine — runs Analysis, Build, Test, Document
  sequentially with gate checks and execution report. Usually invoked via sn-do or
  when user says pipeline orchestrator. Supports autonomous smart defaults, CREATE
  UPDATE DELETE intents, and analyze-only mode.
disable-model-invocation: true
---

# ServiceNow Pipeline Orchestrator (engine)

**Prefer natural language entry**: [sn-do/SKILL.md](../sn-do/SKILL.md) — user says *"pipeline orchestrator add a field"* and `sn-do` parses + calls this skill.

**Single entry**: requirement → four phases → `pipeline-execution-report.md`.

## Identity

**Pipeline Orchestrator** — execute four agent skills in sequence; verify gates; report results.

**Anti-hallucination**: Phase passes only if artifact **exists on disk** and gates pass ([pipeline-gates.md](../servicenow-spec-workflow/references/pipeline-gates.md)).

## Natural language input (via sn-do or direct)

Read [operation-intents.md](../servicenow-spec-workflow/references/operation-intents.md):

1. Parse CREATE / UPDATE / DELETE / ANALYZE_ONLY
2. Detect entity (incident default)
3. Apply autonomous defaults for missing field names, types, form surface
4. Normalize → `requirement/requirement.md`

Direct invoke still works:
```
/sn-pipeline-orchestrator
[requirement]
```

## Modes

| Mode | Default? | Behavior |
|------|----------|----------|
| **autonomous** | **Yes** | [default-decisions.md](../servicenow-spec-workflow/references/default-decisions.md); handoff READY with §3 filled |
| **strict** | Opt-in | Stop on BLOCKING gaps; user says "strict" |
| **analyze_only** | Opt-in | Phase 1 only; user says "don't build" / "just analyze" |

## Sub-agent skills

| Order | Skill | Phase |
|-------|-------|-------|
| 1 | [sn-analysis-agent](../sn-analysis-agent/SKILL.md) | Analyze |
| 2 | [sn-development-agent](../sn-development-agent/SKILL.md) | Build |
| 3 | [sn-testing-agent](../sn-testing-agent/SKILL.md) | Test |
| 4 | [sn-documentation-agent](../sn-documentation-agent/SKILL.md) | Document |

Also: [session-protocol.md](../servicenow-spec-workflow/references/session-protocol.md)

## Pipeline algorithm

```
START
  mode = autonomous (unless strict)
  analyze_only = true if user said don't build / just analyze

  PHASE 1 — ANALYSIS (+ bootstrap session)
    Execute sn-analysis-agent
    Verify G0, G1
    IF analyze_only → REPORT (analysis complete) → END
    IF G1 FAIL in strict → REPORT_FAILED → END
    IF G1 FAIL in autonomous → only if HARD STOP; else fix via defaults and continue

  PHASE 2 — BUILD
    Execute sn-development-agent; Verify G2

  PHASE 3 — TEST
    Execute sn-testing-agent; Verify G3
    Rework loop max 2 if FAIL

  PHASE 4 — DOCUMENT
    Execute sn-documentation-agent; Verify G4

  PHASE 5 — LEARNING HARVEST (mandatory)
    Read session/learnings.md (or harvest from logs)
    Promote per self-learning-protocol.md → learnings-registry.md
    Patch target skills if new HIGH-confidence patterns

  Write pipeline-execution-report.md; chat scorecard
END
```

Read at start: [learnings-registry.md](../servicenow-spec-workflow/references/learnings-registry.md)

## Autonomous + vague requirements

For "add a field to incident form" with no name/type:

- Analysis **must** propose field name, type, ACLs, form placement using operation-intents defaults
- handoff status = **READY FOR DEVELOPMENT** with §3 documenting every DEFAULT
- Build **proceeds** with proposed values unless user previously objected

This is intentional for remote chatbot delivery.

## Final deliverable

`stories/<session_id>/pipeline-execution-report.md`

Update `session.json` → `pipeline` block.

## Chat scorecard

Always output phase ✅/❌ summary + session path + top assumptions from §3.

**Delivery messaging (L002)**:
- If all **FUNCTIONAL** ACs pass on dev → tell user **"Done on dev — nothing required from you."**
- Migration/packaging notes → deploy runbook only, not "your next steps"
- Pipeline **SUCCESS** when functional delivery complete; packaging gaps ≠ PARTIAL unless user asked for migration proof

## Self-learning

After Phase 4: run [self-learning-protocol.md](../servicenow-spec-workflow/references/self-learning-protocol.md). Include § **Learnings promoted** in pipeline report.

User says *recheck skills* → scan recent `learnings.md` + promote + reconcile workflow files.

## DO NOT

- Default to strict unless user requested
- Require formal requirement templates
- Skip report on full pipeline runs
- Deploy to production via MCP
