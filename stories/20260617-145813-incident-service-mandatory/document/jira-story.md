# Jira Story — Make Service Field Mandatory on Incident Form

**Session**: 20260617-145813-incident-service-mandatory  
**Jira Key**: SN-DO-SERVICE-MAND  
**Status**: Complete on dev

---

## 1. Executive Summary

The **Service** field (`business_service`) is now mandatory on the incident form. Users cannot save an incident without selecting a business service. Enforcement uses a Data Policy (server) and UI Policy (client asterisk) scoped to the `incident` table only.

## 2. Original Requirement

See [requirement/requirement.md](../requirement/requirement.md).

## 3. Design Decisions

| Decision | Value | Source |
|----------|-------|--------|
| Field | business_service (label: Service) | Discovery |
| Pattern | UI Policy + Data Policy | DEFAULT |
| Scope | incident table only (not task dictionary) | DEFAULT |
| Conditions | Always mandatory | DEFAULT |

## 4. Solution Architecture

```
Incident Form (classic)
    ├── UI Policy [SN-DO] Incident Service Mandatory
    │   └── Action: business_service → mandatory=true
    └── Data Policy [SN-DO] Incident Service Mandatory
        └── Rule: business_service → mandatory=true
```

## 5. Implementation Record

| Type | Name | sys_id | Purpose |
|------|------|--------|---------|
| Update Set | [20260617-145813-incident-service-mandatory] Incident Service Mandatory | ad2e07d12ba1479015a9f5685e91bfba | Migration package |
| Data Policy | [SN-DO] Incident Service Mandatory - Data Policy | 692e47d12ba1479015a9f5685e91bf0e | Server enforcement |
| Data Policy Rule | business_service | a92e47d12ba1479015a9f5685e91bf3c | Field rule |
| UI Policy | [SN-DO] Incident Service Mandatory - UI Policy | 2d2e47d12ba1479015a9f5685e91bf42 | Client asterisk |
| UI Policy Action | business_service | fd2e47d12ba1479015a9f5685e91bf62 | Mandatory action |

## 6. Update Set

- **Name**: [20260617-145813-incident-service-mandatory] Incident Service Mandatory
- **sys_id**: ad2e07d12ba1479015a9f5685e91bfba
- **Components**: 5
- **State**: in progress

## 7. Testing Summary

| AC | Result |
|----|--------|
| AC-1 Data Policy | PASS |
| AC-2 UI Policy | PASS |
| AC-3 Server validation | PASS |
| AC-4 Update Set packaging | PASS |

**Overall**: PASS

## 8. Deployment Runbook

1. Complete Update Set on dev
2. Export / migrate to test
3. Verify incident form shows red asterisk on Service
4. Attempt save without Service — should be blocked
5. Promote to prod per change process

## 9. Rollback

Set `active=false` on UI Policy (2d2e47d12ba1479015a9f5685e91bf42) and Data Policy (692e47d12ba1479015a9f5685e91bf0e), or revert Update Set.

## 10. Support / Troubleshooting

| Symptom | Check |
|---------|-------|
| No asterisk on form | UI Policy active? Cache cleared? |
| Save allowed without Service | Data Policy active? Rule mandatory=true? |
| Other task types affected | Should not — policies scoped to incident |

## 11. Session Reference

`stories/20260617-145813-incident-service-mandatory/`

## 12. Jira Description (copy-paste)

```
h2. Summary
Make Service (business_service) mandatory on incident form.

h2. Solution
* Data Policy on incident table — server-side mandatory
* UI Policy on incident table — client-side asterisk

h2. Testing
All ACs passed on accenture-demo dev instance.

h2. Deployment
Complete Update Set [20260617-145813-incident-service-mandatory] Incident Service Mandatory and migrate.
```
