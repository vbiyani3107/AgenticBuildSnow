# Artifact Revert Catalog

**Default action for pipeline CREATE artifacts: deactivate (`active=false`).**  
**Never hard-delete** unless user explicitly requests delete of a custom-only record.

Revert order: **children before parents**, **dependents before dependencies**.

## Catalog

| Pipeline artifact | Table | Revert action | Order | Verify |
|-------------------|-------|---------------|-------|--------|
| UI Policy Action | sys_ui_policy_action | Deactivate or delete child only if policy kept | 1 (child) | mandatory/visible actions gone |
| UI Policy | sys_ui_policy | active=false | 2 | active=false |
| Data Policy Rule | sys_data_policy_rule | Deactivate rule | 1 (child) | mandatory=false or inactive |
| Data Policy | sys_data_policy2 | active=false | 2 | active=false |
| Business Rule | sys_script | active=false | 1 | active=false |
| Client Script | sys_script_client | active=false | 1 | active=false |
| Script Include | sys_script_include | active=false | 1 | active=false |
| Notification | sysevent_email_action | active=false | 1 | active=false |
| Event | sysevent_register | active=false | 2 | active=false |
| Assignment Rule | sysrule_assignment | active=false | 1 | active=false |
| Scheduled Job | sysauto_script | active=false | 1 | active=false |
| ACL | sys_security_acl | active=false | 1 | active=false |
| Dictionary field (CREATE) | sys_dictionary | active=false on element | 2 | element inactive |
| Choice | sys_choice | inactive or delete child | 1 (child) | choices gone |
| Form element | sys_ui_element | Remove from form only if pipeline added | 1 | element absent from form |
| Flow | sys_hub_flow | Deactivate flow | 1 | active=false |
| Module | sys_app_module | active=false | 1 | active=false |
| Fix Script | sys_script_fix | active=false (do not execute) | 1 | active=false |
| Update Set | sys_update_set | state=ignore OR leave in progress | last | not migrated |

## Pipeline UPDATE artifacts

| Change type | Revert strategy |
|-------------|-----------------|
| Set mandatory=true (dictionary) | Set mandatory=false on same dictionary row |
| Set mandatory via policy | Deactivate policy (CREATE path) |
| Changed label/choice | Restore from discovery-notes.md if captured; else STOP — ask user |
| Modified OOB record | **HARD STOP** — inform user |

## Hard stops (inform user — do not proceed)

- OOB artifact (no `[SN-DO]` / session naming pattern and not in implementation-log)
- Artifact already deployed to prod (revert dev + document human prod steps)
- Dependency query shows other active config references artifact
- sys_id in log does not match record on instance (possible wrong environment)

## Partial revert

User may request subset (e.g. "revert only UI policy"). Execute only listed rows; report remaining active artifacts explicitly.

## Functional verification (inverse of pipeline AC)

| Original AC | Revert verify |
|-------------|---------------|
| Field mandatory | Save without field succeeds |
| BR sets field | Field no longer auto-set |
| Notification sends | Notification inactive — no send |
| Scheduled job runs | Job inactive — no execution |
