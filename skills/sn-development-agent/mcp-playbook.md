# MCP Playbook — Build Agent

Server: **`user-servicenow-demo`** | Catalog: [platform-artifact-catalog.md](../servicenow-spec-workflow/references/platform-artifact-catalog.md)

Inspect tool JSON schema before first use each session.

## Session start

```
SN-Get-Current-Instance
SN-Get-Current-Update-Set
SN-List-Update-Sets
SN-Set-Current-Application (if scoped)
```

## Artifact → table → MCP

| Artifact | Table | Create | Verify query |
|----------|-------|--------|--------------|
| Business Rule | `sys_script` | SN-Create-Record | name, collection, when |
| Script Include | `sys_script_include` | SN-Create-Record | name, client_callable |
| Client Script | `sys_script_client` | SN-Create-Record | name, table, type |
| UI Policy | `sys_ui_policy` | SN-Create-Record | name, table, conditions |
| UI Policy Action | `sys_ui_policy_action` | SN-Batch-Create / BG script | policy + field |
| Data Policy | `sys_data_policy2` | SN-Create-Record | name, table |
| ACL | `sys_security_acl` | SN-Create-Record | name, operation, role |
| Assignment Rule | `sysrule_assignment` | SN-Create-Record | name, order, table |
| Notification | `sysevent_email_action` | SN-Create-Record | name, event_name |
| Event | `sysevent_register` | SN-Create-Record | event_name |
| Scheduled Job | `sysauto_script` | SN-Create-Record **or BG script** (see L003) | name, run_type |
| Fix Script | `sys_script_fix` | SN-Create-Record | name — **manual run** |
| Dictionary | `sys_dictionary` | SN-Create-Record | name, element |
| Choice | `sys_choice` | SN-Create-Record | element, value |
| Module | `sys_app_module` | SN-Create-Record | title, name |
| Flow | `sys_hub_flow` | SN-Create-Workflow + publish | handoff-specific |
| Catalog item | `sc_cat_item` | SN-Create-Record | SN-Validate-Configuration |

## Write patterns

| Pattern | Tool |
|---------|------|
| Single record | SN-Create-Record / SN-Update-Record |
| Parent + children | SN-Batch-Create with `save_as` |
| Bulk update | SN-Batch-Update |
| REST-blocked fields | SN-Execute-Background-Script (trigger) |
| Set current Update Set | SN-Set-Update-Set → SN-Execute-Background-Script |
| Move to US | SN-Move-Records-To-Update-Set |

### REST limitations

- `catalog_ui_policy_action`: ui_policy + catalog_variable via background script
- UI Policy Action references: batch or background script
- Update Set current: never REST-only
- **Metadata create + US capture (L001, L003)**: prefer single `SN-Execute-Background-Script` after `GlideUpdateSet.set(usId)` with `gr.insert()` — REST `SN-Create-Record` often skips `sys_update_xml`

### Update Set + metadata create pattern (L001, L003)

```javascript
// Preferred: create in same script as US set
var us = new GlideUpdateSet();
us.set('<update_set_sys_id>');
var gr = new GlideRecord('sysauto_script');
gr.initialize();
gr.name = '[SN-DO] ...';
gr.run_type = 'daily';
gr.run_time = '1970-01-01 15:00:00';
gr.active = true;
gr.script = '...';
var id = gr.insert();
gs.info('Created sysauto_script: ' + id);
```

After create: verify `sys_update_xml` by time/name; retry once programmatically before noting packaging gap.

## Resolve references by name (no hardcoding)

```
sys_user_group     → SN-Query-Table name=<group>
sys_user           → SN-List-SysUsers / query user_name
cmdb_ci            → SN-List-CmdbCis / query name
sys_choice         → SN-Explain-Field for element
```

Log resolved sys_id in implementation-log once — reuse within session.

## ITSM test operations

| Module | Tools |
|--------|-------|
| Incident | SN-Create-Incident, Assign, Resolve, Close, Add-Work-Notes |
| Change | SN-List-ChangeRequests, Assign-Change, Approve-Change |
| Problem | SN-List-Problems, Close-Problem, Add-Problem-Comment |

## Update Set closure

```
SN-Inspect-Update-Set (show_dependencies: true if handoff requires)
→ log components in implementation-log
```

## Do not use without handoff

SN-Demo-*, SN-Deploy-Demo

## Error handling

| Error | Action |
|-------|--------|
| 401/403 | BLOCKED — auth |
| Wrong instance | STOP — fix MCP |
| Duplicate name | Query first; UPDATE if handoff says modify |
| Transaction fail | Log ops; BLOCKED |

## Evidence file format (build/evidence/step-N.md)

```markdown
Step N: [title]
Query: table=..., query=...
Result: [sys_id, key fields]
Expected: [from handoff]
PASS | FAIL
```
