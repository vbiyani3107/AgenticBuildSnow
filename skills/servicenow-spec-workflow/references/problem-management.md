# Problem Management Module Reference

Use when module is `problem-management` or requirement references problems, root cause, known errors.

## Core tables

| Table | Purpose |
|-------|---------|
| `problem` | Problem records (extends `task`) |
| `problem_task` | Problem tasks |
| `incident` | Linked via `problem_id` / related lists |

Key fields: `state`, `problem_state`, `root_cause`, `cause_notes`, `fix`, `workaround`, `known_error`, `related_incidents`.

## Lifecycle (typical)

| State | Label |
|-------|-------|
| 1 | New |
| 2 | Assess |
| 3 | Root Cause Analysis |
| 4 | Fix in Progress |
| 5 | Resolved |
| 6 | Closed |

## Common artifacts

| Need | Artifacts |
|------|-----------|
| Link incidents to problem | Related list, BR, Flow |
| Known error database | Knowledge article + problem flag |
| Root cause mandatory | UI Policy / Data Policy on state transition |
| Workaround field | Dictionary + form layout |
| Auto-create from trend | PA / Flow (advanced) |

## MCP tools

`SN-List-Problems`, `SN-Add-Problem-Comment`, `SN-Close-Problem`, `SN-Query-Table` on `problem`

## Analysis checklist

- [ ] Problem vs incident scope clear?
- [ ] Known error / KCS article needed?
- [ ] RCA fields mandatory on which state?
- [ ] Impact on incident resolution workflow?
- [ ] Major problem / major incident correlation?

## Testing

- Create problem → state transitions with mandatory fields
- Link incident → verify relationship
- Resolve problem → verify linked incident behavior (per handoff)

## Anti-patterns

- Closing problem while linked incidents still open (unless handoff specifies)
- Duplicate root cause on incident instead of problem record
