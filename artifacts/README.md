# Portable ServiceNow artifacts

Deployable scripts and metadata exported from **AgenticBuildSnow** pipeline sessions. Use these to recreate configuration on other instances without re-running the full pipeline.

## Artifacts

| Folder | Artifact | Table |
|--------|----------|-------|
| [daily-incident-list-job/](daily-incident-list-job/) | `[SN-DO] Daily Top 10 Incidents List` | `sysauto_script` |

## How to use

1. Open the artifact folder README.
2. Run `sysauto_script-recreate.js` (or equivalent) in **Scripts - Background** or via MCP.
3. Verify in the target instance UI.

Session history and evidence remain under `.cursor/servicenow-sessions/<session_id>/`.
