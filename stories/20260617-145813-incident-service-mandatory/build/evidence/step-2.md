Step 2: UI Policy + Action
Query: table=sys_ui_policy, short_description=[SN-DO] Incident Service Mandatory - UI Policy
Result: sys_id=2d2e47d12ba1479015a9f5685e91bf42, active=true, table=incident
Query: table=sys_ui_policy_action, field=business_service^table=incident
Result: sys_id=fd2e47d12ba1479015a9f5685e91bf62, mandatory=true
Expected: UI policy active with mandatory action for business_service
PASS
