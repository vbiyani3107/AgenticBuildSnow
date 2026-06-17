# ServiceNow SDLC — Remote Development via Chatbot

Maps standard ServiceNow SDLC to the four-agent pipeline. All agents align to this lifecycle.

---

## Standard SN SDLC phases → Our agents

| SN SDLC phase | Activities | Our agent | Session artifacts |
|---------------|------------|-----------|-------------------|
| **1. Intake / Refinement** | Requirement, scope, acceptance | Analysis | `requirement/`, `analyze/handoff.md` |
| **2. Design** | Artifact selection, security, data model | Analysis | handoff §5 Technical Design |
| **3. Build / Configure** | Update Set, metadata, scripts | Build | `build/implementation-log.md` |
| **4. Unit / Config test** | Self-verify per step | Build | `build/evidence/` |
| **5. QA / SIT** | Acceptance criteria, regression | Test | `test/test-report.md` |
| **6. Documentation** | Runbook, Jira, deployment notes | Document | `document/jira-story.md` |
| **7. Deploy** | Complete US, migrate, post-deploy | Human + doc | handoff §10 + jira §Deployment |
| **8. Verify / Close** | Smoke test prod, close story | Human | test report reference |

Remote chatbot covers phases **1–6**; phases **7–8** require human approval for production.

---

## Update Set lifecycle (mandatory in Build)

```
Create/select Update Set
    → Set current (background script if needed)
    → Set application scope (if scoped)
    → Make changes (all captured in US)
    → Inspect Update Set (components + dependencies)
    → Self-verify each change
    → Complete Update Set (human in target env)
    → Migrate dev → test → prod
```

Document Update Set name + sys_id in `session.json` and implementation log.

---

## Environment promotion

| Env | Remote MCP | Agent behavior |
|-----|------------|----------------|
| Dev / Personal Developer Instance | Yes — primary | Build + Test default here |
| Test / UAT | Maybe — if MCP configured | Test report notes env |
| Production | Rarely via MCP | Document only; HARD STOP without explicit approval |

Default: all Build/Test on MCP-connected instance. Jira doc includes promotion checklist for human.

---

## Quality gates (SDLC)

| Gate | Criteria | Owner |
|------|----------|-------|
| G1 Design complete | handoff READY; ACs defined | Analysis |
| G2 Build complete | All steps DONE/BLOCKED; US inspected | Build |
| G3 Test pass | All AC PASS or accepted PARTIAL | Test |
| G4 Doc complete | Jira story with deployment + rollback | Document |
| G5 Release ready | Human completes US; migrates | Human |

---

## Example walkthrough — Incident P1 auto-assignment

**Requirement**: "When P1 network incident is created, assign to Network Support and notify duty manager."

### Phase 1 — Analysis (autonomous defaults applied)

| Decision | Value | Source |
|----------|-------|--------|
| Instance | dev via MCP | DEFAULT |
| Update Set | `INC-1234 P1 network assign` | DEFAULT |
| Assignment | Assignment Rule before BR | DEFAULT |
| Notification | Event + Email Notification | DEFAULT |
| Table | `incident` not `task` | DEFAULT |

**Artifacts designed**:
1. Assignment Rule — condition: priority=1, category=network
2. Notification — event: incident.assigned, condition: priority=1

**ACs**:
- AC1: Create P1 network incident → assignment_group = Network Support
- AC2: Create P2 network incident → NOT auto-assigned to Network Support
- AC3: Notification record generated on P1 assign

### Phase 2 — Build

| Step | Action | Verify |
|------|--------|--------|
| 0 | Set Update Set | SN-Get-Current-Update-Set |
| 1 | Query Network Support group sys_id by name | SN-Query-Table sys_user_group |
| 2 | Create Assignment Rule | SN-Create-Record sysrule_assignment |
| 3 | Create Notification | SN-Batch-Create |
| 4 | Inspect Update Set | SN-Inspect-Update-Set |

### Phase 3 — Test

| AC | Result | Evidence |
|----|--------|----------|
| AC1 | PASS | incident sys_id; assignment_group verified |
| AC2 | PASS | P2 incident different group |
| AC3 | PASS | sysevent_email_action or sys_email queried |

### Phase 4 — Document

Jira story includes: summary, artifacts table, US name, deployment steps, rollback (deactivate assignment rule + notification).

---

## Example — UI Policy before Client Script

**Requirement**: "Show root cause field when state is Resolved on incident form."

**Analysis selects**: UI Policy on `incident` — condition `state==6` — action show `cause` (or custom field).

**NOT**: Client Script onChange unless field is dynamic variable.

---

## Example — Fix Script vs Business Rule

**Requirement**: "Set category=network on all open incidents where short_description contains 'VPN'."

**Analysis selects**:
- **One-time**: Fix Script in Update Set, manual execute post-deploy, query limit 500/batch
- **NOT**: Permanent BR (unless requirement says "ongoing")

---

## Example — Change request CAB (future module)

**Requirement**: "Standard changes skip CAB; normal changes need CAB approval."

**Analysis**: Flow on `change_request` with condition on `type`; Approval activity for normal.

Reference: [change-management.md](change-management.md)

---

## Rework loop (SDLC defect fix)

```
Test FAIL → gap report → Build rework run → Test re-run → Document append revision
```

Same session folder; `phases.build.rework_count` incremented.

---

## Autonomous progression

Remote chatbot SDLC does **not** wait indefinitely:

1. Analysis asks once → defaults → READY
2. Build executes → logs blockers
3. Test validates → documents MCP limits
4. Document captures truth including assumptions

User reviews artifacts asynchronously; corrects via new instruction or rework.

---

## Related references

- [default-decisions.md](default-decisions.md)
- [platform-artifact-catalog.md](platform-artifact-catalog.md)
- [servicenow-best-practices.md](servicenow-best-practices.md)
