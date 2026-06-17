---
name: servicenow-spec-workflow
description: >-
  Orchestrates spec-driven remote ServiceNow development — one Cursor session
  equals one session folder with analyze, build, test, document subfolders linked
  via session.json. Four agents, SDLC alignment, autonomous defaults. Use for SN
  spec workflow, per-story sessions, or Incident/Change/Problem delivery.
disable-model-invocation: true
---

# ServiceNow Spec-Driven Workflow — Remote Development

**Vision**: Full ServiceNow SDLC via chatbot — one Cursor session = one story = one linked folder. Agents progress autonomously when user is unavailable, applying documented best-practice defaults.

## Core references (read as needed)

| Doc | Purpose |
|-----|---------|
| [session-protocol.md](references/session-protocol.md) | Session folders, linking |
| [sdlc-remote-development.md](references/sdlc-remote-development.md) | SDLC mapping + examples |
| [default-decisions.md](references/default-decisions.md) | **Auto-answer when user silent** |
| [platform-artifact-catalog.md](references/platform-artifact-catalog.md) | All SN artifact types |
| [servicenow-best-practices.md](references/servicenow-best-practices.md) | Development standards |
| [self-learning-protocol.md](references/self-learning-protocol.md) | **Capture + promote learnings** |
| [learnings-registry.md](references/learnings-registry.md) | **Validated patterns from past runs** |
| [incident-management.md](references/incident-management.md) | Default module |
| [change-management.md](references/change-management.md) | Change lifecycle |
| [problem-management.md](references/problem-management.md) | Problem lifecycle |

## Session layout

```
stories/<session_id>/
├── SESSION.md + session.json
├── learnings.md
├── requirement/requirement.md
├── analyze/    SPEC.md, handoff.md, discovery-notes.md
├── build/      SPEC.md, implementation-log.md, evidence/
├── test/       SPEC.md, test-report.md, evidence/
└── document/   SPEC.md, jira-story.md
```

## Pipeline

```
/sn-analysis-agent  → analyze/handoff.md     (design + defaults)
/sn-development-agent → build/implementation-log.md
/sn-testing-agent   → test/test-report.md
/sn-documentation-agent → document/jira-story.md
```

Rework: test FAIL → build (same session) → test again.

| Document | `/sn-documentation-agent` | Jira + deployment doc |
| **Full pipeline** | `/sn-pipeline-orchestrator` | **All 4 phases + execution report** |

## Pipeline orchestrator

Single entry: paste requirement → runs Analyze → Build → Test → Document with gate verification.

Skill: `sn-pipeline-orchestrator` | Gates: [references/pipeline-gates.md](references/pipeline-gates.md)

Modes: **strict** (default, minimal assumptions) | **autonomous** (apply defaults)

Output: `pipeline-execution-report.md` in session folder with phase scorecard.

## Agents

| Invoke | Role |
|--------|------|
| `/sn-analysis-agent` | Bootstrap session, design, handoff |
| `/sn-development-agent` | MCP build on dev instance |
| `/sn-testing-agent` | Independent AC validation |
| `/sn-documentation-agent` | Jira + deployment doc |

## Autonomous remote development

1. Analysis asks clarifying questions **once**
2. User silent / says continue → apply [default-decisions.md](references/default-decisions.md)
3. Document every default in handoff §3
4. Build → Test → Document without re-asking resolved defaults
5. Production deploy always **human** — documented in jira-story

## Self-learning (mandatory)

After every pipeline run, agents follow [self-learning-protocol.md](references/self-learning-protocol.md):

1. Write `learnings.md` in session folder
2. Promote durable patterns to [learnings-registry.md](references/learnings-registry.md)
3. Patch target skills (mcp-playbook, gates, agent SKILLs) when confidence HIGH
4. **Analysis + Build**: read registry at session start and apply matching patterns

User trigger: *"recheck skills"* / *"self learning"* → scan recent sessions, promote, reconcile all workflow files.

## Platform coverage

Handles any artifact in [platform-artifact-catalog.md](references/platform-artifact-catalog.md): UI Policies, Data Policies, Client Scripts, Business Rules, Script Includes, Fix Scripts, Scheduled Jobs, Flows, Notifications, ACLs, Modules, Dashboards, Catalog, integrations — extensible by adding catalog rows + module refs.

## MCP

Server: **`user-servicenow-demo`**. Dev/subprod only unless user explicitly approves prod.

## Templates

[templates/session/](templates/session/) — session bootstrap  
[templates/handoff-template.md](templates/handoff-template.md) — binding design spec
