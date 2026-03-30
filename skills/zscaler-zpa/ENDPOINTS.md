<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->
# Zscaler Private Access (ZPA) API Reference

### API Keys (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/apiKeys` | Get all apiKeys details |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/apiKeys` | Create api keys for customer |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/apiKeys/{{id}}` | Get apiKeys details by id |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/apiKeys/{{id}}` | Update api keys by id |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/apiKeys/{{id}}` | Delete apiKeys |

### Admin SSO Configuration (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ssoLoginOptions` | Get SSO Login Details |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ssoLoginOptions` | Update SSO Options for Customer |

### Administrators (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/administrators/{{adminId}}` | Get Administrator details |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/administrators/{{adminId}}` | Update details of administrator |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/administrators/{{adminId}}` | Delete Administrator by Id |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/administrators` | Get all administrators |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/administrators` | Create Administrator |

### Application Controller (21 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}/mappings` | Get the Application Segment Mapping details |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/configured/count` | Returns the count of configured application Segment |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/configured/currentAndMaxLimit` | Get current applications count and maxLimit |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/summary` | Get all application id and names |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/export` | Export Application Segments |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application` | Gets all configured Application Segments |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/application` | Adds a new Application Segment |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/provision` | Provision a new application (creates all related objects) |
| GET | `/mgmtconfig/v1/admin/customers/{customerId}/application/multimatchUnsupportedReferences` | Get unsupported multimatch references |
| PUT | `/mgmtconfig/v1/admin/customers/{customerId}/application/bulkUpdateMultiMatch` | Bulk update multimatch in multiple applications |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}` | Gets the Application Segment by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}/weightedLbConfig` | Get Weighted Load Balancer Config |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}/weightedLbConfig` | Update Weighted Load Balancer Config |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}` | Updates the Application Segment by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}` | Deletes the Application Segment by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/getAppsByType` | Get all BA/Inspect/PRA Application Segments |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/getAppByType` | Get all BA/Inspect/PRA Application Segments (alt) |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}/deleteAppByType` | Delete a BA/Inspection/PRA application |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}/share` | Share Application Segment to microtenants |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/{{applicationId}}/move` | Move application between microtenants |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/application/validate` | Validate conflicting wildcard domain names |

### Branch Connector Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/branchConnector` | Get all BranchConnectors |

### Branch Connector Group Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/branchConnectorGroup/summary` | Get all BranchConnector Groups Summary |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/branchConnectorGroup` | Get all BranchConnector Groups |

### Browser Protection Profile Controller (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/activeBrowserProtectionProfile` | Get the active browser protection profiles |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/browserProtectionProfile` | Gets all configured browser protection profiles |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/browserProtectionProfile/setActive/{{browserProtectionProfileId}}` | Set a browser protection profile as active |

### CBI Banner Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/banners/{{bannerId}}` | Get CBI Banner by ID |
| PUT | `/cbiconfig/cbi/api/customers/{{customerId}}/banners/{{bannerId}}` | Update CBI Banner by ID |
| DELETE | `/cbiconfig/cbi/api/customers/{{customerId}}/banners/{{bannerId}}` | Delete CBI Banner by ID |
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/banners` | Get all CBI Banners |
| POST | `/cbiconfig/cbi/api/customers/{{customerId}}/banner` | Add a CBI Banner |

### CBI Certificate Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/certificates` | Get all CBI Certificates |
| POST | `/cbiconfig/cbi/api/customers/{{customerId}}/certificate` | Add a CBI Certificate |
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/certificates/{{certificateId}}` | Get CBI Certificate by ID |
| PUT | `/cbiconfig/cbi/api/customers/{{customerId}}/certificates/{{certificateId}}` | Update CBI Certificate by ID |
| DELETE | `/cbiconfig/cbi/api/customers/{{customerId}}/certificates/{{certificateId}}` | Delete CBI Certificate by ID |

### CBI Profile Controller (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/zpaprofiles` | Get all CBI Profiles in ZPA |
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/profiles/{{profileId}}` | Get CBI profile by ID |
| PUT | `/cbiconfig/cbi/api/customers/{{customerId}}/profiles/{{profileId}}` | Update CBI profile by ID |
| DELETE | `/cbiconfig/cbi/api/customers/{{customerId}}/profiles/{{profileId}}` | Delete CBI profile by ID |
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/regions` | Get all CBI Regions |
| GET | `/cbiconfig/cbi/api/customers/{{customerId}}/profiles` | Get all CBI Profiles |
| POST | `/cbiconfig/cbi/api/customers/{{customerId}}/profiles` | Add a CBI profile |

### Certificate Controller (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/clientlessCertificate/{{certificateId}}` | Get certificate by ID (deprecated) |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/clientlessCertificate/issued` | Get all issued certificates (deprecated) |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/certificate` | Gets all certificates |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/certificate` | Add a certificate with private key |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/certificate/issued` | Gets all issued certificates |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/certificate/{{certificateId}}` | Gets certificate by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/certificate/{{certificateId}}` | Deletes certificate by ID |

### Cloud Connector Group Controller (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/cloudConnectorGroup/{{id}}` | Get Cloud Connector Group by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/cloudConnectorGroup/summary` | Get all Cloud Connector Group summaries |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/cloudConnectorGroup` | Gets all Cloud Connector Groups |

### Cloud Connector Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/cloudConnectorGroup/{{id}}` | Get all EdgeConnectors |

### Connector Controller (9 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/connector/bulkDelete` | Bulk delete App Connectors |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/connector/{{connectorId}}` | Get App Connector by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/connector/{{connectorId}}` | Update App Connector by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/connector/{{connectorId}}/update` | Trigger update of the Connector |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/connector/{{connectorId}}` | Delete App Connector by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/connector` | Gets all App Connectors |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/connectorSchedule/{{id}}` | Update connector cleanup schedule |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/connectorSchedule` | Get connector cleanup schedule |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/connectorSchedule` | Create connector cleanup schedule |

### Connector Group Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/appConnectorGroup/{{appConnectorGroupId}}` | Get App Connector Group by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/appConnectorGroup/{{appConnectorGroupId}}` | Update App Connector Group by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/appConnectorGroup/{{appConnectorGroupId}}` | Delete App Connector Group by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/appConnectorGroup` | Gets all App Connector Groups |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/appConnectorGroup/summary` | Get all App Connector Group names/IDs |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/appConnectorGroup` | Add a new App Connector Group |

### Client Settings Controller (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{customerId}/clientSetting` | Get clientSetting details |
| GET | `/mgmtconfig/v1/admin/customers/{customerId}/clientSetting/all` | Get all clientSetting details |
| DELETE | `/mgmtconfig/v1/admin/customers/{customerId}/clientSetting` | Delete a client setting |
| POST | `/mgmtconfig/v1/admin/customers/{customerId}/clientSetting` | Create or update client setting |

### Customer Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/authDomains` | Gets authentication domains |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}` | Get customer details by customerId |

### Customer Version Profile Controller (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/visible/versionProfiles` | Gets all visible Version Profiles |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/versionProfiles` | Get associated version profiles |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/versionProfiles/{{versionProfileId}}` | Update Version Profile |

### Customer Config Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/config/isZiaCloudConfigAvailable` | Check ZIA cloud config availability |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/config/isZiaCloudConfig` | Get ZIA cloud service config |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/config/isZiaCloudConfig` | Add/update ZIA cloud service config |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/config/sessionTerminationOnReauth` | Get session termination on reauth setting |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/config/sessionTerminationOnReauth` | Update session termination on reauth |

### Customer Domain Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/associationtype/{{type}}/domains` | Get domains for customer |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/associationtype/{{type}}/domains` | Add/update domains for customer |

### Customer DR Tool Version Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/customerDRToolVersion` | Fetch latest DR Tool Versions |

### C2C IP Ranges Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ipRanges` | Get all IP Ranges |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ipRanges/search` | Search IP Ranges by page |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ipRanges` | Add a new IP Range |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ipRanges/{{ipRangeId}}` | Get IP Range by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ipRanges/{{ipRangeId}}` | Update IP Range by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/v2/ipRanges/{{ipRangeId}}` | Delete IP Range by ID |

### Emergency Access Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/emergencyAccess/user/{{userId}}` | Get emergency access user |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/emergencyAccess/user/{{userId}}` | Update emergency access user |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/emergencyAccess/user/{{userId}}/deactivate` | Deactivate emergency access user |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/emergencyAccess/user/{{userId}}/activate` | Activate emergency access user |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/emergencyAccess/users` | Get all emergency access users |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/emergencyAccess/user` | Create emergency access user |

### Enrollment Certificate Controller (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/enrollmentCert` | Gets all enrollment certificates |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/enrollmentCert/{{enrollmentCertId}}` | Get enrollment certificate by ID |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/enrollmentCert/csr/generate` | Generate enrollment cert CSR |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/enrollmentCert` | Create enrollment cert |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/enrollmentCert/selfsigned/generate` | Create self-signed enrollment cert |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/enrollmentCert/{{enrollmentCertId}}` | Update enrollment cert |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/enrollmentCert/{{enrollmentCertId}}` | Delete enrollment cert |

### Extranet Resource Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/extranetResource/partner` | Retrieve extranet resource endpoints |

### IdP Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/idp` | Gets all configured IdPs |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/idp/{{idpId}}` | Gets IdP by ID |

### Inspection Control Controller (14 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/controlTypes` | Get inspection control types |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/custom` | Get all custom controls |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/custom` | Add a new custom control |
| GET | `/mgmtconfig/v1/admin/inspectionControls/customControlTypes` | Get custom control types |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/custom/{{id}}/profiles` | Get inspection profiles for control |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/custom/httpMethods` | Get supported HTTP methods in custom controls |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/severityTypes` | Get inspection severity types |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/custom/{{id}}` | Get custom control by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/custom/{{id}}` | Update custom control by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/custom/{{id}}` | Delete custom control by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/predefined/versions` | Get predefined control versions |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/actionTypes` | Get inspection action types |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/predefined/{{id}}` | Get predefined control by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionControls/predefined` | Get all predefined controls |

### Inspection Profile Controller (9 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile/{{inspectionProfileId}}/dissociateAllPredefinedControls` | Dissociate all predefined controls from profile |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile` | Get all inspection profiles |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile` | Add a new inspection profile |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile/{{inspectionProfileId}}/associateAllPredefinedControls` | Associate all predefined controls to profile |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile/{{inspectionProfileId}}` | Get inspection profile by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile/{{inspectionProfileId}}` | Update inspection profile by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile/{{inspectionProfileId}}` | Delete inspection profile by ID |
| PATCH | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile/{{inspectionProfileId}}/patch` | Patch inspection profile and controls |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/inspectionProfile/{{inspectionProfileId}}/deAssociateAllPredefinedControls` | Dissociate all predefined controls (deprecated) |

### Isolation Profile Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/isolation/profiles` | Gets all isolation profiles |

### Location Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/location/extranetResource/{{zpnErId}}` | Retrieve Extranet Location Resource |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/location/summary` | Get all Location names/IDs |

### Location Group Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/locationGroup/extranetResource/{{zpnErId}}` | Retrieve Extranet Location Group Resource |

### Log Streaming Service (LSS) Configuration Controller (10 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/lssConfig/{{lssId}}` | Get LSS config by ID |
| PUT | `/mgmtconfig/v2/admin/customers/{{customerId}}/lssConfig/{{lssId}}` | Update LSS config by ID |
| DELETE | `/mgmtconfig/v2/admin/customers/{{customerId}}/lssConfig/{{lssId}}` | Delete LSS config by ID |
| GET | `/mgmtconfig/v2/admin/lssConfig/logType/formats` | Get all LSS log formats |
| GET | `/mgmtconfig/v2/admin/lssConfig/clientTypes` | Get all LSS client types (deprecated) |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/lssConfig` | Get all LSS configs |
| POST | `/mgmtconfig/v2/admin/customers/{{customerId}}/lssConfig` | Add a new LSS config |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/lssConfig/logType/formats` | Get LSS log formats for customer |
| GET | `/mgmtconfig/v2/admin/lssConfig/statusCodes` | Get LSS status codes |
| GET | `/mgmtconfig/v2/admin/lssConfig/customers/{{customerId}}/clientTypes` | Get LSS client types for customer |

### Machine Group Controller (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/machineGroup/{{Id}}` | Get Machine Group by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/machineGroup` | Get all Machine Groups |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/machineGroup/summary` | Get all Machine Group names/IDs |

### Microtenant Controller (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/microtenants/{{microtenantId}}` | Get Microtenant by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/microtenants/{{microtenantId}}` | Update Microtenant by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/microtenants/{{microtenantId}}` | Delete Microtenant by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/microtenants/summary` | Get Microtenant names/IDs |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/microtenants` | Gets all Microtenants |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/microtenants` | Add a new Microtenant |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/microtenants/search` | Search Microtenants with filters |
| GET | `/mgmtconfig/v1/admin/me` | Get current session details |

### Managed Browser Profile Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/managedBrowserProfile/search` | Get all managed browser profiles |

### NPClient Endpoints (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/vpnConnectedUsers` | Get all VPN connected users |

### OAuth2 User Code Verification Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/{{associationType}}/usercodes` | Verify user codes for provisioning |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/{{associationType}}/usercodes/status` | User code provisioning status |

### Permission Groups (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/permissionGroups` | Get all default permission groups |

### Policy Set Controller (15 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/policyType/{{policyType}}` | Get policy set by type |
| POST | `/mgmtconfig/v2/admin/customers/{{customerId}}/policySet/{{policySetId}}/rule` | Add policy rule (v2) |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/{{policySetId}}/rule` | Add policy rule (v1) |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/{{policySetId}}/reorder` | Bulk reorder all rules in a policy set |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/platform` | Get all platforms |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/{{policySetId}}/rule/{{ruleId}}/reorder/{{newOrder}}` | Reorder a single rule |
| PUT | `/mgmtconfig/v2/admin/customers/{{customerId}}/policySet/{{policySetId}}/rule/{{ruleId}}` | Update policy rule (v2) |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/rules/policyType/{{policyType}}` | Get paginated rules by policy type |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/clientTypes` | Get all client types |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/{{policySetId}}/rule/{{ruleId}}` | Get rule by ID |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/riskScoreValues` | Get risk score values |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/policySet/rules/policyType/{{policyType}}/count` | Get policy rule count |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/policySet/rules/policyType/{{policyType}}/application/{{applicationId}}` | Get rules by policy type and app ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/{{policySetId}}/rule/{{ruleId}}` | Update policy rule (v1) |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/policySet/{{policySetId}}/rule/{{ruleId}}` | Delete policy rule |

### Posture Profile Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/posture/{{id}}` | Get posture profile by ID |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/posture` | Get all posture profiles |

### PRA Approval Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/approval` | Get all privileged approvals |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/approval` | Add a new privileged approval |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/approval/{{id}}` | Get privileged approval by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/approval/{{id}}` | Update privileged approval by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/approval/{{id}}` | Delete privileged approval by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/approval/expired` | Delete all expired approvals |

### PRA Credential Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/credential/{{id}}/move` | Move credential between microtenants |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/credential` | Get all privileged credentials |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/credential` | Add a new privileged credential |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/credential/{{id}}` | Get privileged credential by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/credential/{{id}}` | Update privileged credential by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/credential/{{id}}` | Delete privileged credential by ID |

### PRA Credential Pool Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/waap-pra-config/v1/admin/customers/{{customerId}}/credential-pool` | Get all credential pools |
| GET | `/waap-pra-config/v1/admin/customers/{{customerId}}/credential-pool/{{id}}` | Get credential pool by ID |
| PUT | `/waap-pra-config/v1/admin/customers/{{customerId}}/credential-pool/{{id}}` | Update credential pool by ID |
| DELETE | `/waap-pra-config/v1/admin/customers/{{customerId}}/credential-pool/{{id}}` | Delete credential pool by ID |
| POST | `/waap-pra-config/v1/admin/customers/{{customerId}}/credential-pool` | Add a new credential pool |
| GET | `/waap-pra-config/v1/admin/customers/{{customerId}}/credential-pool/{{id}}/credential` | Get credentials mapped to pool |

### PRA Console Controller (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/praConsole/praPortal/{{portalId}}` | Get consoles for portal |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/praConsole` | Get all privileged consoles |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/praConsole` | Add a new privileged console |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/praConsole/{{id}}` | Get privileged console by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/praConsole/{{id}}` | Update privileged console by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/praConsole/{{id}}` | Delete privileged console by ID |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/praConsole/bulk` | Bulk create privileged consoles |

### PRA Portal Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/praPortal` | Get all privileged portals |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/praPortal` | Add a new privileged portal |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/praPortal/{{id}}` | Get privileged portal by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/praPortal/{{id}}` | Update privileged portal by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/praPortal/{{id}}` | Delete privileged portal by ID |

### Private Cloud Group Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudControllerGroup` | Get all Private Cloud Controller Groups |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudControllerGroup/summary` | Get Private Cloud Controller Group names/IDs |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudControllerGroup/{{privateCloudControllerGroupId}}` | Update Private Cloud Controller Group |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudControllerGroup/{{privateCloudControllerGroupId}}` | Delete Private Cloud Controller Group |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudControllerGroup/{{privateCloudControllerGroupId}}` | Get Private Cloud Controller Group by ID |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudControllerGroup` | Add a new Private Cloud Controller Group |

### Private Cloud Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudController` | Get all Private Cloud Controllers |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudController/{{privateCloudControllerId}}` | Get Private Cloud Controller by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudController/{{privateCloudControllerId}}` | Update Private Cloud Controller |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudController/{{privateCloudControllerId}}/restart` | Trigger restart of Private Cloud Controller |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/privateCloudController/{{privateCloudControllerId}}` | Delete Private Cloud Controller |

### Provisioning Key Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/associationType/{{associationType}}/provisioningKey/{{provisioningKeyId}}` | Get Provisioning Key by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/associationType/{{associationType}}/zcomponent/{{zcomponentId}}/provisioningKey` | Get Provisioning Key by zcomponentId |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/associationType/{{associationType}}/provisioningKey/{{provisioningKeyId}}` | Update Provisioning Key |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/associationType/{{associationType}}/provisioningKey/{{provisioningKeyId}}` | Delete Provisioning Key |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/associationType/{{associationType}}/provisioningKey` | Gets all Provisioning Keys |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/associationType/{{associationType}}/provisioningKey` | Add a new Provisioning Key |

### Role Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/roles/{{roleId}}` | Get role by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/roles/{{roleId}}` | Update a Role |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/roles/{{roleId}}` | Delete a Role |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/roles` | Get all roles |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/administrators` | Create Administrator |

### SAML Attribute Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/samlAttribute` | Get all SAML attributes |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/samlAttribute/idp/{{idpId}}` | Get SAML attributes by IdP |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/samlAttribute/{{attrId}}` | Get SAML attribute by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/samlAttribute/{{attrId}}` | Delete SAML attribute |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/samlAttribute/{{attrId}}` | Update SAML attribute |
| POST | `/mgmtconfig/v2/admin/customers/{{customerId}}/samlAttribute` | Add a new SAML attribute |

### SCIM Attribute Header Controller (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/idp/{{idpId}}/scimattribute` | Get all SCIM attributes for IdP |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/idp/{{idpId}}/scimattribute/{{scimAttributeId}}` | Get SCIM attribute by ID |
| GET | `/userconfig/v1/customers/{{customerId}}/scimattribute/idpId/{{idpId}}/attributeId/{{attributeId}}` | Get SCIM attribute values |

### SCIM Group Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/userconfig/v1/customers/{{customerId}}/scimgroup/{{scimGroupId}}` | Get SCIM Group by ID |
| GET | `/userconfig/v1/customers/{{customerId}}/scimgroup/idpId/{{idpId}}` | Get all SCIM groups for IdP |

### Segment Group Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/segmentGroup/{{segmentGroupId}}` | Get Segment Group by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/segmentGroup/{{segmentGroupId}}` | Update Segment Group (v1) |
| PUT | `/mgmtconfig/v2/admin/customers/{{customerId}}/segmentGroup/{{segmentGroupId}}` | Update Segment Group (v2) |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/segmentGroup/{{segmentGroupId}}` | Delete Segment Group |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/segmentGroup` | Get all Segment Groups |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/segmentGroup` | Add a new Segment Group |

### Server Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/server` | Get all Servers |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/server` | Add a new Server |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/server/{{serverId}}` | Get Server by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/server/summary` | Get all Server names/IDs |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/server/{{serverId}}` | Update Server by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/server/{{serverId}}` | Delete Server by ID |

### Service Edge Controller (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeSchedule/{{id}}` | Update Service Edge cleanup schedule |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeSchedule` | Get Service Edge cleanup schedule |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeSchedule` | Create Service Edge cleanup schedule |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdge/{{serviceEdgeId}}` | Get Service Edge by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdge/{{serviceEdgeId}}` | Update Service Edge by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdge/{{serviceEdgeId}}` | Delete Service Edge by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdge` | Get all Service Edges |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdge/bulkDelete` | Bulk delete Service Edges |

### Service Edge Group Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeGroup/{{serviceEdgeGroupId}}` | Get Service Edge Group by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeGroup/{{serviceEdgeGroupId}}` | Update Service Edge Group |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeGroup/{{serviceEdgeGroupId}}` | Delete Service Edge Group |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeGroup` | Get all Service Edge Groups |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/serviceEdgeGroup` | Add a new Service Edge Group |

### Server Group Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serverGroup` | Get all Server Groups |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serverGroup/summary` | Get all Server Group names/IDs |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/serverGroup` | Add a new Server Group |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/serverGroup/{{groupId}}` | Get Server Group by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/serverGroup/{{groupId}}` | Update Server Group by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/serverGroup/{{groupId}}` | Delete Server Group by ID |

### Tag Group Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/tagGroup/search` | Search Tag Groups |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/tagGroup` | Add new Tag Group |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/tagGroup/{{tagGroupId}}` | Get Tag Group by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/tagGroup/{{tagGroupId}}` | Update Tag Group by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/tagGroup/{{tagGroupId}}` | Delete Tag Group by ID |

### Tag Key Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}/tagKey/search` | Search Tag Keys |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}/tagKey` | Add new Tag Key |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}/tagKey/{{tagKeyId}}` | Get Tag Key by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}/tagKey/{{tagKeyId}}` | Update Tag Key by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}/tagKey/bulkUpdateStatus` | Bulk enable/disable Tag Keys |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}/tagKey/{{tagKeyId}}` | Delete Tag Key by ID |

### Tag Namespace Controller (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/search` | Search Tag Namespaces |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace` | Add new Tag Namespace |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}` | Get Tag Namespace by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}` | Update Tag Namespace by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/status` | Enable/disable predefined Namespace |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/namespace/{{namespaceId}}` | Delete Tag Namespace by ID |

### Trusted Network Controller (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/network/{{id}}` | Get trusted network by ID |
| GET | `/mgmtconfig/v2/admin/customers/{{customerId}}/network` | Get all trusted networks |

### Step Up Auth Level Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/stepupauthlevel` | Get step up auth levels |

### User Portal Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortal` | Get all User Portals |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortal` | Add a new User Portal |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortal/{{id}}` | Get User Portal by ID |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortal/{{id}}` | Update User Portal by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortal/{{id}}` | Delete User Portal by ID |

### User Portal Link Controller (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortalLink` | Get all User Portal Links |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortalLink` | Add a new User Portal Link |
| POST | `/mgmtconfig/v2/admin/customers/{{customerId}}/userPortalLink/bulk` | Bulk add User Portal Links |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortalLink/{{id}}` | Get User Portal Link by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortalLink/userPortal/{{portalId}}` | Get User Portal Links for a Portal |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortalLink/{{id}}` | Update User Portal Link |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/userPortalLink/{{id}}` | Delete User Portal Link |

### User Portal AUP Controller (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/userportal/aup` | Get all AUPs |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/userportal/aup/{{id}}` | Get AUP by ID |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/userportal/aup` | Add a new AUP |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/userportal/aup/{{id}}` | Update AUP by ID |
| DELETE | `/mgmtconfig/v1/admin/customers/{{customerId}}/userportal/aup/{{id}}` | Delete AUP by ID |

### Workload Tag Group Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/workloadTagGroup/summary` | Retrieve Workload Tag Group |

### Zscaler Path Cloud Controller (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/zpathCloud/getAltClouds` | Get all alternate clouds for zpath |

### Zscaler Path Config Override (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/configOverrides/{{id}}` | Get config-override by ID |
| GET | `/mgmtconfig/v1/admin/customers/{{customerId}}/configOverrides` | Get all config-overrides |
| POST | `/mgmtconfig/v1/admin/customers/{{customerId}}/configOverrides` | Create config-override |
| PUT | `/mgmtconfig/v1/admin/customers/{{customerId}}/configOverrides/{{id}}` | Update config-override |

