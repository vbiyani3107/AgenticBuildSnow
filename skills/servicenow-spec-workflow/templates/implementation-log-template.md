# Implementation Log Template

**Session ID**: 
**Session folder**: `.cursor/servicenow-sessions/<session_id>/`
**Handoff Reference**: `analyze/handoff.md`
**Developer Agent Run**: [date/time]
**Instance**: [name + URL from SN-Get-Current-Instance]
**Update Set**: [name + sys_id]

---

## Pre-flight Checklist

- [ ] Read `analyze/handoff.md` completely
- [ ] SN-Get-Current-Instance — confirmed correct target
- [ ] Update Set set and verified (SN-Get-Current-Update-Set)
- [ ] Application scope set if required (SN-Set-Current-Application)
- [ ] No BLOCKING open questions in handoff (or user waived)

## Step Execution Log

| Step # | Handoff Step | Status | sys_id / Artifact | Self-Verification | Notes |
|--------|--------------|--------|-------------------|-------------------|-------|
| 0 | Pre-flight | DONE | | | |
| 1 | | DONE / BLOCKED / SKIPPED | | PASS / FAIL | |

### Step Detail (repeat per step)

#### Step [N]: [title]

**Action taken**:

**MCP tools used**:

**Records created/updated** (table, sys_id, key fields):

**Self-verification**:
- Query/inspect used:
- Result:
- PASS / FAIL

---

## Update Set Inspection

**Tool**: SN-Inspect-Update-Set
**Components captured**:

| Type | Name | sys_id |
|------|------|--------|

**Missing dependencies** (if any):

## Deviations from Handoff

| Handoff instruction | What was done instead | Reason | User approved? |
|---------------------|----------------------|--------|----------------|

**Rule**: No deviations without documenting here. Prefer BLOCKED over silent deviation.

## Blocked Items

| Step | Blocker | Needs |
|------|---------|-------|

## Handoff to Testing Agent

- [ ] All in-scope steps DONE or explicitly BLOCKED with reason
- [ ] Self-verification PASS for each completed step
- [ ] Update Set inspection complete
- [ ] Acceptance criteria in handoff unchanged (or Analysis updated)

**Ready for Testing**: YES / NO
