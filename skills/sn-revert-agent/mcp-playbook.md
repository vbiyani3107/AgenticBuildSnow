# MCP Playbook — Revert Agent

Server: **`user-servicenow-demo`**

Inspect tool JSON schema before first use each session.

## Session start

```
SN-Get-Current-Instance     → must match source session.json
SN-Get-Current-Update-Set   → note current US (do not assume)
```

## Read (inventory proof)

| Source | Tool |
|--------|------|
| Artifact exists | SN-Get-Record / SN-Query-Table by sys_id |
| Artifact by name | SN-Query-Table name/short_description query |
| Update Set contents | SN-Inspect-Update-Set |
| Dependencies | SN-Inspect-Update-Set show_dependencies: true |

## Write (revert)

| Action | Tool | Notes |
|--------|------|-------|
| Deactivate single record | SN-Update-Record `{ active: false }` | Preferred |
| Batch deactivate | SN-Batch-Update | Same table, transaction: true |
| REST-blocked / ordered deactivate | SN-Execute-Background-Script | Child-first in one script |
| New revert Update Set | SN-Execute-Background-Script | GlideUpdateSet.set() in same script |

### Background script pattern (deactivate + US capture)

```javascript
var usName = '[<revert_id>] Revert <source_session_id>';
var usGr = new GlideRecord('sys_update_set');
usGr.addQuery('name', usName);
usGr.query();
var usId = usGr.next() ? usGr.getUniqueValue() : usGr.insert();
new GlideUpdateSet().set(usId);

function deactivate(table, sysId) {
  var gr = new GlideRecord(table);
  if (!gr.get(sysId)) return 'MISSING';
  if (gr.active == false) return 'ALREADY_INACTIVE';
  gr.active = false;
  gr.update();
  return 'DEACTIVATED';
}

// Child-first order — example
gs.info(deactivate('sys_ui_policy_action', '<act_sys_id>'));
gs.info(deactivate('sys_ui_policy', '<ui_sys_id>'));
gs.info(deactivate('sys_data_policy_rule', '<rule_sys_id>'));
gs.info(deactivate('sys_data_policy2', '<dp_sys_id>'));
```

## Verify after revert

| Check | Query |
|-------|-------|
| Policy inactive | `active=false` on artifact table |
| Functional undo | Background script or SN-Create-Incident smoke test per handoff AC inverse |

## Do not use

| Tool | Why |
|------|-----|
| SN-Demo-Revert | Demo teardown by prefix — not pipeline scope |
| deleteRecord in scripts | Default forbidden — deactivate only |

## Error handling

| Error | Action |
|-------|--------|
| 401/403 | BLOCKED — auth |
| Wrong instance | STOP — inform user |
| Record not found | SKIPPED — log in report |
| OOB / scoped mismatch | STOP — inform user |

## Evidence format (`reverts/<id>/evidence/step-N.md`)

```markdown
Step N: Deactivate <artifact name>
Table: sys_ui_policy
sys_id: <id>
Before: active=true
Action: SN-Update-Record active=false
After: active=false
Result: PASS | SKIPPED | FAIL
```
