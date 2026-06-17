# AgenticBuildSnow

Agentic ServiceNow development workflow for Cursor — natural-language requests run through a full **Analyze → Build → Test → Document** pipeline with MCP integration on a dev instance.

## What this repo contains

```
AgenticBuildSnow/
├── stories/           ← Your ServiceNow stories (pipeline artifacts)
├── artifacts/         ← Portable deploy scripts (recreate on any instance)
├── skills/            ← sn-do pipeline skills + spec workflow
└── .cursor/
    └── rules/         ← Cursor-only: route SN requests to sn-do
```

| Path | Purpose |
|------|---------|
| `stories/` | **Per-story folders** — requirements, handoff, build log, tests, docs |
| `artifacts/` | Portable deploy scripts to recreate ServiceNow config on other instances |
| `skills/` | Cursor agent skills (`sn-do`, orchestrator, analysis/build/test/document, spec workflow) |
| `.cursor/rules/` | Workspace rule to auto-route ServiceNow requests to `sn-do` |

---

## End-to-end workflow (full guide)

### Overview

```
You (natural language in Cursor)
        │
        ▼
   /sn-do  ──►  Analyze  ──►  Build (MCP)  ──►  Test  ──►  Document
        │            │              │              │            │
        │            ▼              ▼              ▼            ▼
        │      stories/<id>/   ServiceNow    evidence     jira-story.md
        │      handoff.md      dev instance  test-report  + learnings
        │
        └──► artifacts/ (optional portable deploy package)
```

One Cursor chat = one story = one folder under `stories/<session_id>/`.

---

### Step 0 — One-time setup

#### 1. Clone the repo

```bash
git clone https://github.com/vbiyani3107/AgenticBuildSnow.git
cd AgenticBuildSnow
```

Open this folder as your **Cursor workspace** (File → Open Folder).

#### 2. Install skills into Cursor

Copy pipeline skills so Cursor can find them:

```bash
cp -R skills/* ~/.cursor/skills/
```

Skills installed: `sn-do`, `sn-pipeline-orchestrator`, `sn-analysis-agent`, `sn-development-agent`, `sn-testing-agent`, `sn-documentation-agent`, `servicenow-spec-workflow`.

#### 3. Connect ServiceNow MCP

- Enable MCP server **`user-servicenow-demo`** in Cursor settings.
- Point it at your **dev / subprod** instance (not production unless explicitly approved).
- Verify connection: the agent can call `SN-Get-Current-Instance`.

#### 4. Workspace rule (already in repo)

`.cursor/rules/servicenow-remote-dev.mdc` routes casual ServiceNow requests to `sn-do` automatically when this repo is open.

---

### Step 1 — Start a new story

**Best practice:** open a **new Cursor chat** per story.

Ask in plain English — no Jira key or API names required:

```
/sn-do create a global scheduled job to run daily at 3 PM and list 10 incidents (read-only). Run full pipeline.
```

Other examples:

```
/sn-do add a mandatory field on the incident classic form for external ticket ID

Pipeline orchestrator — update the assignment rule for P1 network incidents

/sn-do delete the test business rule from incident — just analyze first
```

**Modes:**

| You say | What happens |
|---------|----------------|
| *(nothing special)* | **Autonomous** — smart defaults, full pipeline |
| `analyze only` / `don't build` | Design only → stops after Analyze |
| `strict` | Stops on blocking gaps instead of defaulting |

---

### Step 2 — Analyze (design)

**Agent:** `sn-analysis-agent`

**Creates:**

```
stories/<session_id>/
├── SESSION.md
├── session.json
├── learnings.md
├── requirement/requirement.md      ← your verbatim ask
└── analyze/
    ├── handoff.md                ← binding spec for build
    └── discovery-notes.md        ← MCP read-only findings
```

**You get in chat:** parsed intent, assumptions (§3 in handoff), handoff status **READY FOR DEVELOPMENT**.

If you only wanted analysis, stop here. Otherwise the pipeline continues automatically.

---

### Step 3 — Build (implement on dev)

**Agent:** `sn-development-agent` via MCP on your dev instance

**Creates / updates on ServiceNow:**

- Records (fields, business rules, scheduled jobs, UI policies, flows, etc.)
- Update Set (when applicable)

**Creates in repo:**

```
stories/<session_id>/build/
├── implementation-log.md         ← what was built, sys_ids
└── evidence/step-*.md            ← per-step MCP verification
```

**You get in chat:** artifact names, sys_ids, Update Set name. When functional delivery is complete: **you're done on dev — nothing required from you.**

---

### Step 4 — Test (verify)

**Agent:** `sn-testing-agent`

**Creates:**

```
stories/<session_id>/test/
├── test-report.md                ← PASS / PARTIAL / FAIL per AC
└── evidence/ac-*.md              ← independent test proof
```

Tests acceptance criteria from `analyze/handoff.md` — happy path, negative, regression.

---

### Step 5 — Document (close story)

**Agent:** `sn-documentation-agent`

**Creates:**

```
stories/<session_id>/document/jira-story.md
stories/<session_id>/pipeline-execution-report.md   ← phase scorecard
```

Updates `session.json` → `status: completed`, `learnings.md` promoted to skills registry when applicable.

---

### Step 6 — Commit your story to Git

After a pipeline run, commit the new story folder:

```bash
git add stories/<session_id>/ artifacts/   # if deploy artifact was added
git commit -m "Add story: <short description>"
git push origin main
```

**What goes in Git vs ServiceNow:**

| In Git (`stories/`) | On ServiceNow (dev instance) |
|---------------------|------------------------------|
| Design, evidence, docs | Live config (jobs, rules, fields…) |
| Script source in handoff | Running scheduled jobs / BRs |
| sys_ids for traceability | Update Sets |

---

### Step 7 — Deploy to another instance (optional)

For portable deliverables under `artifacts/`:

1. Open `artifacts/<artifact-name>/README.md`
2. Run `sysauto_script-recreate.js` in **System Definition → Scripts - Background**
3. Verify in **Scheduled Jobs** (or relevant table)
4. Complete Update Set → migrate test → prod (human approval)

Example: [`artifacts/daily-incident-list-job/`](artifacts/daily-incident-list-job/)

---

### Run individual phases (advanced)

You don't have to run the full pipeline every time:

| Invoke | Phase only |
|--------|------------|
| `/sn-analysis-agent` | Design + handoff |
| `/sn-development-agent` | Build (needs existing handoff) |
| `/sn-testing-agent` | Test (needs build log) |
| `/sn-documentation-agent` | Doc (needs test report) |
| `/sn-pipeline-orchestrator` | Full engine (usually via `/sn-do`) |

**Rework:** if Test fails, fix in the same chat — build appends a rework section, then re-test.

---

### Self-learning

Each story writes `stories/<session_id>/learnings.md`. Durable patterns are promoted to:

`skills/servicenow-spec-workflow/references/learnings-registry.md`

Say **"recheck skills"** in chat to scan recent stories and update workflow files.

---

### Example walkthrough (completed story)

**Ask:** daily scheduled job, list 10 incidents read-only at 3 PM.

| Step | Result |
|------|--------|
| Story folder | [`stories/20260617-090539-daily-incident-list-job/`](stories/20260617-090539-daily-incident-list-job/) |
| Live job on dev | `[SN-DO] Daily Top 10 Incidents List` |
| Deploy package | [`artifacts/daily-incident-list-job/`](artifacts/daily-incident-list-job/) |
| Final doc | `stories/.../document/jira-story.md` |

---

## Pipeline phases (quick reference)

| Phase | Skill | Output |
|-------|-------|--------|
| Analyze | `sn-analysis-agent` | `analyze/handoff.md` |
| Build | `sn-development-agent` | `build/implementation-log.md` |
| Test | `sn-testing-agent` | `test/test-report.md` |
| Document | `sn-documentation-agent` | `document/jira-story.md` |

Entry point: **`/sn-do`** (natural language) or **`/sn-pipeline-orchestrator`** (engine).

---

## Example sessions

| Session | Story | Portable artifact |
|---------|-------|-------------------|
| `20260617-090539-daily-incident-list-job` | Daily scheduled job — list top 10 incidents (read-only) at 3 PM | `artifacts/daily-incident-list-job/` |
| `20250617-120000-incident-new-field` | Incident custom field (analysis) | — |

See [`stories/INDEX.md`](stories/INDEX.md) for all stories.

---

## Related

The ServiceNow MCP connector may live in a sibling project (`demoenvservicenowmcp/`) — not included here (separate repository).

## License

Internal / demo use — adjust as needed for your organization.
