Step 1: Data Policy + Rule
Query: table=sys_data_policy2, short_description=[SN-DO] Incident Service Mandatory - Data Policy
Result: sys_id=692e47d12ba1479015a9f5685e91bf0e, active=true, model_table=incident
Query: table=sys_data_policy_rule, field=business_service
Result: sys_id=a92e47d12ba1479015a9f5685e91bf3c, mandatory=true
Expected: Data policy active with mandatory rule for business_service
PASS
