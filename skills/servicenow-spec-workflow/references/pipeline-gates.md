# Pipeline Gate Verification — Anti-Hallucination Checks

The orchestrator **must not advance** to the next phase until every check for the current phase passes. Verify by **reading files from disk** — never trust chat claims alone.

---

## Gate G0 — Session bootstrap

| # | Check | How to verify |
|---|-------|---------------|
| G0.1 | Session folder exists | Path `.cursor/servicenow-sessions/<session_id>/` |
| G0.2 | session.json valid | Parse JSON; session_id matches folder |
| G0.3 | requirement/requirement.md | Non-empty; contains user requirement text |
| G0.4 | All phase SPEC.md exist | analyze, build, test, document |

**FAIL** → stop pipeline; report "Bootstrap incomplete"

---

## Gate G1 — Analysis complete

| # | Check | How to verify |
|---|-------|---------------|
| G1.1 | analyze/handoff.md exists | Read file |
| G1.2 | Handoff status | Contains `READY FOR DEVELOPMENT` (strict mode) |
| G1.3 | No unresolved BLOCKING | Open Questions table has zero BLOCKING unresolved (strict mode) |
| G1.4 | §3 Assumptions | Every row has Source: USER, DISCOVERY, or DEFAULT (if autonomous) |
| G1.5 | §6 Implementation steps | At least step 0 + one implementation step |
| G1.6 | §9 Acceptance criteria | At least 3 AC rows (happy, negative, regression) |
| G1.7 | session.json | `phases.analyze.status` = completed |
| G1.8 | Discovery | If instance-specific claims in handoff, discovery-notes.md or MCP evidence exists |

**FAIL** → stop pipeline; do **not** start Build. Report missing checks.

**Strict mode**: DEFAULT assumptions without user waiver → FAIL at G1.3/G1.4 unless user enabled autonomous.

---

## Gate G2 — Build complete

| # | Check | How to verify |
|---|-------|---------------|
| G2.1 | build/implementation-log.md exists | Read file |
| G2.2 | Pre-flight checklist | All items checked or BLOCKED documented |
| G2.3 | Step log | Every handoff step has DONE, BLOCKED, or SKIPPED |
| G2.4 | Self-verify | Each DONE step has PASS (not FAIL without rework) |
| G2.5 | Evidence files | At least one `build/evidence/step-*.md` per DONE step |
| G2.6 | Update Set | If metadata changed: inspection section filled |
| G2.7 | Ready for Testing | `Ready for Testing: YES` OR documented NO with blockers |
| G2.8 | session.json | `phases.build.status` = completed |
| G2.9 | MCP evidence | Instance name in log matches SN-Get-Current-Instance from session |

**FAIL** → stop pipeline; do **not** start Test. Report blocked steps.

**Partial BUILD**: If some steps BLOCKED but not critical → continue to Test only if handoff allows; else FAIL.

---

## Gate G3 — Test complete

| # | Check | How to verify |
|---|-------|---------------|
| G3.1 | test/test-report.md exists | Read file |
| G3.2 | Every AC from handoff §9 | Row in results table |
| G3.3 | Evidence | Each AC has PASS/FAIL/BLOCKED — not empty |
| G3.4 | Overall result | Explicit PASS, FAIL, or PARTIAL |
| G3.5 | Build cross-check | Implementation log cross-check section filled |
| G3.6 | session.json | `phases.test.overall_result` set |

**FAIL overall** → trigger rework loop (max 2) → re-run Build gaps only → re-Test → re-verify G2/G3

**PASS or accepted PARTIAL** → proceed to Document

### AC classification (L004 — functional vs packaging)

| Class | Examples | Fail pipeline? |
|-------|----------|----------------|
| **FUNCTIONAL** | Field exists, BR fires, job runs, read-only verified | YES if FAIL |
| **PACKAGING** | Update Set component count, `sys_update_xml` capture | NO — document in deploy runbook; overall **PASS** if all FUNCTIONAL pass |

PACKAGING AC may be `INFO` or `PASS_WITH_NOTE` — not `BLOCKED` requiring user action on dev.

---

## Gate G4 — Document complete

| # | Check | How to verify |
|---|-------|---------------|
| G4.1 | document/jira-story.md exists | Read file |
| G4.2 | Required sections | Summary, Implementation, Testing, Deployment, Rollback |
| G4.3 | Honesty | Test FAIL reflected if applicable |
| G4.4 | session.json | `status` = completed, `active` = false |
| G4.5 | Self-learning | `learnings.md` exists; promotion run per self-learning-protocol.md |

---

## Rework loop limits

| Parameter | Value |
|-----------|-------|
| Max rework cycles | 2 |
| Trigger | Test overall FAIL or PARTIAL with CRITICAL/MAJOR gaps |
| Action | Build reads test-report gaps → append rework → Test again |
| After max | Stop pipeline; report with open gaps |

---

## What is NOT hallucination (allowed)

| Activity | Why |
|----------|-----|
| MCP query results | Evidence from instance |
| DISCOVERY source in §3 | Queried from instance |
| DEFAULT in autonomous mode only | Documented in handoff §3 |
| Inferring artifact type from requirement | Classification per platform catalog — must appear in handoff design table |

## What IS forbidden (orchestrator must catch)

| Violation | Detection |
|-----------|-----------|
| Claiming file written without disk proof | Read file — missing → FAIL |
| Skipping phase | session.json phase status |
| Build without READY handoff | G1.2 |
| PASS test without evidence | G3.3 empty evidence |
| Undocumented deviation | implementation-log Deviations table empty but chat says different |
