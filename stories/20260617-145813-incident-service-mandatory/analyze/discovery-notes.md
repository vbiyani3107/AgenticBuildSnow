# Discovery Notes — 20260617-145813-incident-service-mandatory

**Instance**: accenture-demo (`https://accentureservicessrodemo4.service-now.com`)  
**Date**: 2026-06-17

## Field discovery

| Attribute | Value |
|-----------|-------|
| Element | `business_service` |
| Label | Service |
| Dictionary table | `task` (inherited by `incident`) |
| Type | reference |
| Current mandatory (dictionary) | false |
| Form presence | `sys_ui_element` records exist on incident form |

## Existing policies

| Artifact type | Query | Result |
|---------------|-------|--------|
| UI Policy | incident + service/business_service | None found |
| Data Policy | incident + service/business_service | None found |

## Design decision

No conflicting policies. Create new UI Policy + Data Policy (not dictionary `mandatory=true` — avoids global task impact).
