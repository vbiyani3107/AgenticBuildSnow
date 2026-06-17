# Test Report Template

**Session ID**: 
**Session folder**: `stories/<session_id>/`
**References**: `analyze/handoff.md`, `build/implementation-log.md`
**Testing Agent Run**: [date/time]
**Instance**: [name + URL]
**Tester context**: [role used for testing, e.g. itil / admin — prefer non-admin per AC]

---

## Test Summary

| Metric | Count |
|--------|-------|
| Acceptance criteria | |
| PASS | |
| FAIL | |
| BLOCKED | |
| NOT TESTED | |

**Overall Result**: PASS / FAIL / PARTIAL

---

## Acceptance Criteria Results

| AC# | Criterion (from handoff) | Test Steps Executed | Evidence | Result | Notes |
|-----|--------------------------|---------------------|----------|--------|-------|
| AC1 | | | query result / sys_id | PASS / FAIL / BLOCKED | |

### AC Detail (repeat per criterion)

#### AC[N]: [title]

**Preconditions**:

**Steps**:
1. 

**Expected** (from handoff):

**Actual**:

**Evidence** (MCP query, record snapshot, tool output):

**Result**: PASS / FAIL / BLOCKED

---

## Regression Checks

| Area | Test | Result | Notes |
|------|------|--------|-------|

## Implementation Log Cross-Check

| Impl Step | Claimed Status | Independently Verified | Match? |
|-----------|----------------|--------------------------|--------|

## Failures & Gaps (for Development Agent rework)

| Gap ID | AC# / Step | Description | Severity | Suggested Fix |
|--------|------------|-------------|----------|---------------|
| G1 | | | CRITICAL / MAJOR / MINOR | |

## Blocked Tests

| AC# | Blocker | Owner |
|-----|---------|-------|

## Handoff

- **If PASS**: Ready for `/sn-documentation-agent`
- **If FAIL/PARTIAL**: User re-invokes `/sn-development-agent` with this report; dev appends to `build/implementation-log.md`

**Sign-off**: Testing complete — [date]
