# Change Management Module Reference

Use when `session.json` module is `change-management` or requirement references change requests, CAB, or change lifecycle.

## Core tables

| Table | Purpose |
|-------|---------|
| `change_request` | Change records (extends `task`) |
| `change_task` | Implementation tasks |
| `std_change_record_producer` | Standard change templates |
| `sysapproval_approver` | Approvals |

Key fields: `type` (normal/standard/emergency), `risk`, `impact`, `priority`, `state`, `assignment_group`, `assigned_to`, `start_date`, `end_date`, `cab_required`, `approval`, `backout_plan`, `test_plan`, `implementation_plan`.

## Lifecycle (typical)

| State | Label (typical) |
|-------|-----------------|
| -5 | New |
| -4 | Assess |
| -3 | Authorize |
| -2 | Scheduled |
| -1 | Implement |
| 0 | Review |
| 3 | Closed |
| 4 | Canceled |

Confirm on instance via `SN-Explain-Field` on `change_request.state`.

## Common artifacts

| Need | Artifacts |
|------|-----------|
| CAB approval | Flow with Approval, BR to set approval state |
| Risk auto-calc | BR on assess |
| Standard change | Record producer + template |
| Collision | OOB Change Collision plugin |
| Post-implementation review | BR on state → Review |
| Emergency change | Separate flow path; audit trail |

## MCP tools

`SN-List-ChangeRequests`, `SN-Assign-Change`, `SN-Approve-Change`, `SN-Add-Change-Comment`, `SN-Query-Table` on `change_request`

## Analysis checklist

- [ ] Change type: normal / standard / emergency?
- [ ] CAB required?
- [ ] Approval chain and roles (`change_manager`, `cab_manager`)?
- [ ] Blackout windows / maintenance schedules?
- [ ] CMDB CI affected?
- [ ] Conflict with incident/problem linking?
- [ ] Backout plan mandatory fields?

## Testing scenarios

- Create change by type → verify state path
- Approve / reject → verify state + approval record
- Standard change → verify template applied
- Negative: emergency path should not skip required audit fields

## Anti-patterns

- BR on `task` affecting all task types
- Skipping backout plan on normal changes
- Hardcoded CAB group sys_id
