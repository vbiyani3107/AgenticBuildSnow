# Revert Agent — Examples

## Full session revert

**User:**
```
/sn-revert 20260617-145813-incident-service-mandatory
```

**Agent:**
1. Loads `stories/20260617-145813-incident-service-mandatory/build/implementation-log.md`
2. Builds plan: deactivate UI Policy Action → UI Policy → Data Policy Rule → Data Policy
3. Shows plan + asks confirm (or proceeds if intent explicit)
4. Executes on accenture-demo
5. Writes `reverts/20260617-160000-revert-incident-service-mandatory/revert-report.md`

## Partial revert

**User:**
```
/sn-revert only the UI policy from the service mandatory session
```

**Agent:** Plan includes only `sys_ui_policy` + `sys_ui_policy_action` rows from implementation-log. Data Policy stays active. Reports remaining active artifacts.

## Ambiguous session

**User:**
```
revert my last pipeline work
```

**Agent:** Lists `stories/INDEX.md` completed sessions → user picks one → plan → execute.

## Blocked — migrated to prod

**Agent informs:**
> Session was documented for migration. I can deactivate artifacts on **dev** only. Test/prod require human Update Set backout. Proceed on dev?

## Blocked — OOB artifact

**Agent informs:**
> `Caller` dictionary mandatory is OOB and not in pipeline implementation-log. I will not modify it. Only pipeline artifacts are in scope.

## Hard delete request

**User:**
```
delete those policies completely
```

**Agent:**
> Default is deactivate (recoverable). Hard delete is irreversible. Confirm: deactivate (recommended) or delete?
