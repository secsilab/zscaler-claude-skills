<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->
# Zscaler Internet Access (ZIA) API Reference

### Activation (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/status` | Get activation status |
| POST | `/status/activate` | Activate configuration changes |

### Admin Audit Logs (12 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auditlogEntryReport` | Request audit log report (supports filters: actions, category, sub-categories, interface, result, resource, admin ID, client IP) |
| GET | `/auditlogEntryReport` | Get report generation status |
| GET | `/auditlogEntryReport/download` | Download generated report |
| DELETE | `/auditlogEntryReport` | Delete report |

### Advanced Settings (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/advancedSettings` | Get Advanced Settings |
| PUT | `/advancedSettings` | Update Advanced Settings |

### Advanced Threat Protection Policy (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cyberThreatProtection/advancedThreatSettings` | Get Advanced Threat Settings |
| PUT | `/cyberThreatProtection/advancedThreatSettings` | Update Advanced Threat Settings |
| GET | `/cyberThreatProtection/maliciousUrls` | Get Malicious URLs |
| PUT | `/cyberThreatProtection/maliciousUrls` | Update Malicious URLs |
| GET | `/cyberThreatProtection/securityExceptions` | Get Security Exceptions |
| PUT | `/cyberThreatProtection/securityExceptions` | Update Security Exceptions |

### Admin & Role Management (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/adminRoles/lite` | Admin Roles - Get all |
| GET | `/adminUsers` | Admin Users - Get all |
| POST | `/adminUsers` | Admin Users - Add |
| PUT | `/adminUsers/{adminId}` | Admin Users - Update |
| DELETE | `/adminUsers/{adminId}` | Admin Users - Delete |

### Alert Subscriptions (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/alertSubscriptions` | Get all alert subscriptions |
| GET | `/alertSubscriptions/{id}` | Get alert subscription by ID |
| POST | `/alertSubscriptions` | Add alert subscription |
| PUT | `/alertSubscriptions/{id}` | Update alert subscription |
| DELETE | `/alertSubscriptions/{id}` | Delete alert subscription |

### Bandwidth Control & Classes (12 endpoints)

#### Bandwidth Classes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/bandwidthClasses` | Get all bandwidth classes |
| GET | `/bandwidthClasses/{id}` | Get bandwidth class by ID |
| GET | `/bandwidthClasses/lite` | Get all bandwidth classes (lite) |
| POST | `/bandwidthClasses` | Add bandwidth class |
| PUT | `/bandwidthClasses/{id}` | Update bandwidth class |
| DELETE | `/bandwidthClasses/{id}` | Delete bandwidth class |

#### Bandwidth Control Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/bandwidthControlRules` | Get all bandwidth control rules |
| GET | `/bandwidthControlRules/lite` | Get all bandwidth control rules (lite) |
| GET | `/bandwidthControlRules/{id}` | Get bandwidth control rule by ID |
| POST | `/bandwidthControlRules` | Add bandwidth control rule |
| PUT | `/bandwidthControlRules/{id}` | Update bandwidth control rule |
| DELETE | `/bandwidthControlRules/{id}` | Delete bandwidth control rule |

### Browser Control Settings (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/browserControlSettings` | Get Browser Control Settings |
| PUT | `/browserControlSettings` | Update Browser Control Settings |

### Browser Isolation (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/browserIsolation/profiles` | Get all Browser Isolation profiles |

### Cloud Applications (8 endpoints)

#### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cloudApplications/sslPolicy` | Get cloud applications (SSL Policy) |
| GET | `/cloudApplications/policy` | Get cloud applications (Policy) |
| GET | `/cloudApplications/lite` | Get all cloud applications (lite) |
| PUT | `/cloudApplications/bulkUpdate` | Bulk update cloud applications |
| GET | `/customTags` | Get all custom tags |

#### Risk Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/riskProfiles` | Get all risk profiles |
| GET | `/riskProfiles/lite` | Get all risk profiles (lite) |
| GET | `/riskProfiles/{id}` | Get risk profile by ID |
| POST | `/riskProfiles` | Add risk profile |
| PUT | `/riskProfiles/{id}` | Update risk profile |
| DELETE | `/riskProfiles/{id}` | Delete risk profile |

### Cloud App Control Policy (19 endpoints)

#### Cloud Application Instances

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cloudApplicationInstances` | Get all instances |
| GET | `/cloudApplicationInstances/{id}` | Get instance by ID |
| POST | `/cloudApplicationInstances` | Add instance |
| PUT | `/cloudApplicationInstances/{id}` | Update instance |
| DELETE | `/cloudApplicationInstances/{id}` | Delete instance |

#### Tenancy Restriction

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tenancyRestrictionProfile` | Get all tenant profiles |
| GET | `/tenancyRestrictionProfile/{id}` | Get tenant profile by ID |
| POST | `/tenancyRestrictionProfile` | Add tenant profile |
| PUT | `/tenancyRestrictionProfile/{id}` | Update tenant profile |
| DELETE | `/tenancyRestrictionProfile/{id}` | Delete tenant profile |
| GET | `/tenancyRestrictionProfile/app-item-count/{appType}/{itemType}` | Get item count |

#### Web Application Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/webApplicationRules/{rule_type}` | Get all rules by type |
| GET | `/webApplicationRules/ruleTypeMapping` | Get rule type mapping |
| GET | `/webApplicationRules/{rule_type}/{ruleId}` | Get rule by ID |
| POST | `/webApplicationRules/{rule_type}` | Add rule |
| POST | `/webApplicationRules/{rule_type}/duplicate/{ruleId}` | Duplicate rule |
| POST | `/webApplicationRules/{rule_type}` | Get available actions |
| PUT | `/webApplicationRules/{rule_type}/{ruleId}` | Update rule |
| DELETE | `/webApplicationRules/{rule_type}/{ruleId}` | Delete rule |

### Cloud Nanolog Streaming Service (NSS) (14 endpoints)

#### NSS Servers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/nssServers/types` | Get NSS server types |
| GET | `/nssServers` | Get all NSS servers |
| POST | `/nssServers` | Add NSS server |
| PUT | `/nssServers/{id}` | Update NSS server |
| DELETE | `/nssServers/{id}` | Delete NSS server |

#### NSS Feeds

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/nssFeeds` | Get all NSS feeds |
| GET | `/nssFeeds/{id}` | Get NSS feed by ID |
| POST | `/nssFeeds` | Add NSS feed |
| PUT | `/nssFeeds/{id}` | Update NSS feed |
| DELETE | `/nssFeeds/{id}` | Delete NSS feed |
| GET | `/nssFeeds/feedOutputDefaults` | Get feed output format defaults |
| GET | `/nssFeeds/testConnectivity/{feedId}` | Test feed connectivity |
| POST | `/nssFeeds/validateFeedFormat` | Validate feed format |
| GET | `/nssDownload/{nssId}` | Download NSS server appliance info |

### Data Loss Prevention (38 endpoints)

#### DLP Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/webDlpRules` | Get all DLP rules |
| GET | `/webDlpRules/lite` | Get all DLP rules (lite) |
| POST | `/webDlpRules` | Add DLP rule (with or without content inspection) |
| PUT | `/webDlpRules/{ruleId}` | Update DLP rule |
| DELETE | `/webDlpRules/{ruleId}` | Delete DLP rule |

#### DLP Dictionaries

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dlpDictionaries` | Get all dictionaries |
| GET | `/dlpDictionaries/{id}` | Get dictionary by ID |
| GET | `/dlpDictionaries/lite` | Get all dictionaries (lite) |
| GET | `/dlpDictionaries/{dictId}/predefinedIdentifiers` | Get predefined identifiers |
| POST | `/dlpDictionaries` | Add dictionary |
| POST | `/dlpDictionaries/validateDlpPattern` | Validate pattern |
| PUT | `/dlpDictionaries/{id}` | Update dictionary |
| DELETE | `/dlpDictionaries/{id}` | Delete dictionary |

#### DLP Engines

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dlpEngines` | Get all engines |
| GET | `/dlpEngines/{id}` | Get engine by ID |
| GET | `/dlpEngines/lite` | Get all engines (lite) |
| POST | `/dlpEngines` | Add engine |
| POST | `/dlpEngines/validateDlpExpr` | Validate expression |
| PUT | `/dlpEngines/{id}` | Update engine |
| DELETE | `/dlpEngines/{id}` | Delete engine |

#### DLP Notification Templates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dlpNotificationTemplates` | Get all notification templates |
| GET | `/dlpNotificationTemplates/{id}` | Get notification template by ID |
| GET | `/dlpNotificationTemplates/lite` | Get all notification templates (lite) |
| POST | `/dlpNotificationTemplates` | Add notification template |
| PUT | `/dlpNotificationTemplates/{id}` | Update notification template |
| DELETE | `/dlpNotificationTemplates/{id}` | Delete notification template |

#### DLP Incident Receiver

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/icapServers` | Get all ICAP servers |
| GET | `/icapServers/lite` | Get all ICAP servers (lite) |
| GET | `/icapServers/{id}` | Get ICAP server by ID |
| GET | `/incidentReceiverServers` | Get all incident receiver servers |
| GET | `/incidentReceiverServers/lite` | Get all incident receiver servers (lite) |
| GET | `/incidentReceiverServers/{id}` | Get incident receiver server by ID |

#### Index Templates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dlpExactDataMatchSchemas` | Get all Exact Data Match schemas |
| GET | `/dlpExactDataMatchSchemas/lite` | Get all EDM schemas (lite) |
| GET | `/idmprofile` | Get all Indexed Document Match profiles |
| GET | `/idmprofile/lite` | Get all IDM profiles (lite) |

### Device Groups (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/deviceGroups/devices` | Get all devices |
| GET | `/deviceGroups/devices/lite` | Get all devices (lite) |
| GET | `/deviceGroups` | Get all device groups |

### DNS Control Policy (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/firewallDnsRules` | Get all DNS control rules |
| GET | `/firewallDnsRules/{id}` | Get DNS control rule by ID |
| POST | `/firewallDnsRules` | Add DNS control rule |
| PUT | `/firewallDnsRules/{id}` | Update DNS control rule |
| DELETE | `/firewallDnsRules/{id}` | Delete DNS control rule |

### End User Notifications (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/eun` | Get End User Notifications |
| PUT | `/eun` | Update End User Notifications |

### Email Profiles (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/emailRecipientProfile` | Get all email profiles |
| GET | `/emailRecipientProfile/{profileId}` | Get email profile by ID |
| GET | `/emailRecipientProfile/lite` | Get all email profiles (lite) |
| GET | `/emailRecipientProfile/count` | Get email profile count |
| POST | `/emailRecipientProfile` | Add email profile |
| PUT | `/emailRecipientProfile/{profileId}` | Update email profile |
| DELETE | `/emailRecipientProfile/{profileId}` | Delete email profile |

### FTP Control Policy (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ftpSettings` | Get FTP Settings |
| PUT | `/ftpSettings` | Update FTP Settings |

### Event Logs (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/eventlogEntryReport` | Generate event log report |
| GET | `/eventlogEntryReport` | Get report generation status |
| GET | `/eventlogEntryReport/download` | Download event log report |
| DELETE | `/eventlogEntryReport` | Delete event log report |

### Firewall Policies (40 endpoints)

#### Firewall Filtering Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/firewallFilteringRules` | Get all firewall rules |
| GET | `/firewallFilteringRules/{id}` | Get firewall rule by ID |
| POST | `/firewallFilteringRules` | Add firewall rule |
| PUT | `/firewallFilteringRules/{id}` | Update firewall rule |
| DELETE | `/firewallFilteringRules/{id}` | Delete firewall rule |

#### Time Windows

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/timeWindows` | Get all time windows |
| GET | `/timeWindows/lite` | Get all time windows (lite) |

#### Network Applications & Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/networkApplications` | Get all network applications |
| GET | `/networkApplicationGroups` | Get all network application groups |
| POST | `/networkApplicationGroups` | Add network application group |
| PUT | `/networkApplicationGroups/{id}` | Update network application group |
| DELETE | `/networkApplicationGroups/{id}` | Delete network application group |

#### Network Services & Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/networkServices` | Get all network services |
| POST | `/networkServices` | Add network service |
| PUT | `/networkServices/{id}` | Update network service |
| DELETE | `/networkServices/{id}` | Delete network service |
| GET | `/networkServiceGroups` | Get all network service groups |
| POST | `/networkServiceGroups` | Add network service group |
| PUT | `/networkServiceGroups/{id}` | Update network service group |
| DELETE | `/networkServiceGroups/{id}` | Delete network service group |

#### IP Source Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ipSourceGroups` | Get all IP source groups |
| GET | `/ipSourceGroups/lite` | Get all IP source groups (lite) |
| GET | `/ipSourceGroups/{id}` | Get IP source group by ID |
| POST | `/ipSourceGroups` | Add IP source group |
| PUT | `/ipSourceGroups/{id}` | Update IP source group |
| DELETE | `/ipSourceGroups/{id}` | Delete IP source group |
| GET | `/ipSourceGroups/ipv6SourceGroups` | Get all IPv6 source groups |
| GET | `/ipSourceGroups/ipv6SourceGroups/lite` | Get all IPv6 source groups (lite) |

#### IP Destination Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ipDestinationGroups` | Get all IP destination groups |
| GET | `/ipDestinationGroups/lite` | Get all IP destination groups (lite) |
| GET | `/ipDestinationGroups/{id}` | Get IP destination group by ID |
| POST | `/ipDestinationGroups` | Add IP destination group |
| PUT | `/ipDestinationGroups/{id}` | Update IP destination group |
| DELETE | `/ipDestinationGroups/{id}` | Delete IP destination group |
| GET | `/ipDestinationGroups/ipv6DestinationGroups` | Get all IPv6 destination groups |
| GET | `/ipDestinationGroups/ipv6DestinationGroups/lite` | Get all IPv6 destination groups (lite) |

#### Application Services

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/appServices/lite` | Get all application services (lite) |
| GET | `/appServiceGroups/lite` | Get all application service groups (lite) |

### Forwarding Control Policy (18 endpoints)

#### Forwarding Control Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/forwardingRules` | Get all forwarding control rules |
| GET | `/forwardingRules/{id}` | Get forwarding control rule by ID |
| POST | `/forwardingRules` | Add forwarding control rule |
| PUT | `/forwardingRules/{id}` | Update forwarding control rule |
| DELETE | `/forwardingRules/{id}` | Delete forwarding control rule |
| GET | `/dedicatedIPGateways/lite` | Get dedicated IP gateways (lite) |

#### ZPA Gateways

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/zpaGateways` | Get all ZPA gateways |
| GET | `/zpaGateways/{id}` | Get ZPA gateway by ID |
| POST | `/zpaGateways` | Add ZPA gateway |
| PUT | `/zpaGateways/{id}` | Update ZPA gateway |
| DELETE | `/zpaGateways/{id}` | Delete ZPA gateway |

#### Proxy Gateways

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/proxyGateways` | Get all proxy gateways |
| GET | `/proxyGateways/lite` | Get all proxy gateways (lite) |

#### Third-Party Proxies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/proxies` | Get all proxies |
| GET | `/proxies/{id}` | Get proxy by ID |
| GET | `/proxies/lite` | Get all proxies (lite) |
| PUT | `/proxies/{id}` | Update proxy |
| DELETE | `/proxies/{id}` | Delete proxy |

### Intermediate CA Certificates (19 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/intermediateCaCertificate` | Get all certificates |
| GET | `/intermediateCaCertificate/{certId}` | Get certificate by ID |
| GET | `/intermediateCaCertificate/lite` | Get all certificates (lite) |
| GET | `/intermediateCaCertificate/readyToUse` | Get ready-to-use certificates |
| POST | `/intermediateCaCertificate` | Add certificate |
| POST | `/intermediateCaCertificate/keyPair/{certId}` | Generate key pair |
| GET | `/intermediateCaCertificate/downloadPublicKey/{certId}` | Download public key |
| POST | `/intermediateCaCertificate/verifyKeyAttestation/{certId}` | Verify key attestation |
| GET | `/intermediateCaCertificate/downloadAttestation/{certId}` | Download key attestation |
| POST | `/intermediateCaCertificate/generateCsr/{certId}` | Generate CSR |
| GET | `/intermediateCaCertificate/showCsr/{certId}` | Show CSR |
| GET | `/intermediateCaCertificate/downloadCsr/{certId}` | Download CSR |
| POST | `/intermediateCaCertificate/uploadCert/{certId}` | Upload intermediate certificate |
| GET | `/intermediateCaCertificate/showCert/{certId}` | Show certificate |
| POST | `/intermediateCaCertificate/uploadCertChain/{certId}` | Upload certificate chain |
| POST | `/intermediateCaCertificate/finalizeCert/{certId}` | Finalize certificate |
| PUT | `/intermediateCaCertificate/{certId}` | Update certificate |
| PUT | `/intermediateCaCertificate/makeDefault/{certId}` | Make certificate default |
| DELETE | `/intermediateCaCertificate/{certId}` | Delete certificate |

### IPS Control Policy (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/firewallIpsRules` | Get all IPS control rules |
| GET | `/firewallIpsRules/{id}` | Get IPS control rule by ID |
| POST | `/firewallIpsRules` | Add IPS control rule |
| PUT | `/firewallIpsRules/{id}` | Update IPS control rule |
| DELETE | `/firewallIpsRules/{id}` | Delete IPS control rule |

### IoT Report (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/iotDiscovery/deviceTypes` | Get all IoT device types |
| GET | `/iotDiscovery/categories` | Get all IoT categories |
| GET | `/iotDiscovery/classifications` | Get all IoT classifications |
| GET | `/iotDiscovery/deviceList` | Get all IoT devices |

### Location Management (19 endpoints)

#### Locations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/locations` | Get all locations |
| GET | `/locations/lite` | Get all locations (lite) |
| GET | `/locations/{id}` | Get location by ID |
| POST | `/locations` | Add location (with static IP or VPN credentials) |
| PUT | `/locations/{id}` | Update location |
| DELETE | `/locations/{id}` | Delete location |
| POST | `/locations/bulkDelete` | Bulk delete locations |
| GET | `/locations/{id}/sublocations` | Get all sub-locations |
| GET | `/ipAddresses` | Get all IP addresses |
| GET | `/orgProvisioning/ipGreTunnelInfo` | Get GRE tunnel IP addresses |

#### Location Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/locations/groups` | Get all location groups |
| GET | `/locations/groups/lite` | Get all location groups (lite) |
| GET | `/locations/groups/{id}` | Get location group by ID |
| GET | `/locations/groups/count` | Get location group count |

### Malware Protection Policy (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cyberThreatProtection/atpMalwareInspection` | Get Malware Inspection settings |
| PUT | `/cyberThreatProtection/atpMalwareInspection` | Update Malware Inspection settings |
| GET | `/cyberThreatProtection/malwareSettings` | Get Malware Settings |
| PUT | `/cyberThreatProtection/malwareSettings` | Update Malware Settings |
| GET | `/cyberThreatProtection/atpMalwareProtocols` | Get Malware Protocols |
| PUT | `/cyberThreatProtection/atpMalwareProtocols` | Update Malware Protocols |
| GET | `/cyberThreatProtection/malwarePolicy` | Get Malware Policy |
| PUT | `/cyberThreatProtection/malwarePolicy` | Update Malware Policy |

### Mobile Malware Protection (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mobileAdvanceThreatSettings` | Get Mobile Advance Threat Settings |
| PUT | `/mobileAdvanceThreatSettings` | Update Mobile Advance Threat Settings |

### NAT Control Policy (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dnatRules` | Get all NAT control rules |
| GET | `/dnatRules/{id}` | Get NAT control rule by ID |
| POST | `/dnatRules` | Add NAT control rule |
| PUT | `/dnatRules/{id}` | Update NAT control rule |
| DELETE | `/dnatRules/{id}` | Delete NAT control rule |

### Organization Details (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orgInformation` | Get organization information |
| GET | `/orgInformation/lite` | Get organization information (lite) |
| GET | `/subscriptions` | Get organization subscriptions |

### PAC Files (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pacFiles` | Get all PAC files |
| GET | `/pacFiles/{pacId}/version` | Get PAC file versions |
| GET | `/pacFiles/{pacId}/version/{version}` | Get specific PAC file version |
| POST | `/pacFiles/validate` | Validate PAC file |
| POST | `/pacFiles` | Add PAC file |
| POST | `/pacFiles/{pacId}/version/{version}` | Close PAC version |
| PUT | `/pacFiles/{pacId}/version/{pacVersion}/action/pacVersionAction` | Update PAC file |
| DELETE | `/pacFiles/{pacId}` | Delete PAC file |

### Policy Export (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/exportPolicies` | Export all policies |

### Remote Assistance Support (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/remoteAssistance` | Get Remote Assistance preferences |
| PUT | `/remoteAssistance` | Update Remote Assistance preferences |

### Rule Labels (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ruleLabels` | Get all rule labels |
| GET | `/ruleLabels/{id}` | Get rule label by ID |
| POST | `/ruleLabels` | Add rule label |
| PUT | `/ruleLabels/{id}` | Update rule label |
| DELETE | `/ruleLabels/{id}` | Delete rule label |

### Sandbox Report (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sandbox/report/{md5Hash}` | Get sandbox report (full or summary) |
| GET | `/sandbox/report/quota` | Get sandbox report quota |

### Sandbox Settings (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/behavioralAnalysisAdvancedSettings` | Get custom MD5 hash values |
| PUT | `/behavioralAnalysisAdvancedSettings` | Update MD5 hash list |
| GET | `/behavioralAnalysisAdvancedSettings/fileHashCount` | Get file hash quota |

### SaaS Security API (19 endpoints)

#### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/domainProfiles/lite` | Get all domain profiles (lite) |
| GET | `/quarantineTombstoneTemplate/lite` | Get all tombstone templates (lite) |
| GET | `/casbEmailLabel/lite` | Get all CASB email labels (lite) |
| GET | `/casbTenant/{tenantId}/tags/policy` | Get CASB tenant tags |
| GET | `/casbTenant/lite` | Get all CASB tenants (lite) |
| GET | `/casbTenant/scanInfo` | Get CASB tenant scan info |
| GET | `/casbTenant/validate/status/{tenantId}` | Get CASB tenant validation status |

#### CASB DLP Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/casbDlpRules` | Get CASB DLP rules |
| GET | `/casbDlpRules/all` | Get all CASB DLP rules |
| GET | `/casbDlpRules/{ruleId}` | Get CASB DLP rule by ID |
| POST | `/casbDlpRules` | Add CASB DLP rule |
| PUT | `/casbDlpRules/{ruleId}` | Update CASB DLP rule |
| DELETE | `/casbDlpRules/{ruleId}` | Delete CASB DLP rule |

#### CASB Malware Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/casbMalwareRules` | Get CASB malware rules |
| GET | `/casbMalwareRules/all` | Get all CASB malware rules |
| GET | `/casbMalwareRules/{id}` | Get CASB malware rule by ID |
| POST | `/casbMalwareRules` | Add CASB malware rule |
| PUT | `/casbMalwareRules/{id}` | Update CASB malware rule |
| DELETE | `/casbMalwareRules/{ruleId}` | Delete CASB malware rule |

### Security Policy Settings (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/security` | Get allowlist URLs |
| PUT | `/security` | Update allowlist URLs |
| GET | `/security/advanced` | Get denylist URLs |
| PUT | `/security/advanced` | Update denylist URLs |
| POST | `/security/advanced/blacklistUrls` | Add/Remove URLs from denylist (incremental) |

### Service Edges (10 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtualZenNodes` | Get all service edge nodes |
| POST | `/virtualZenNodes` | Add service edge node |
| GET | `/virtualZenNodes/{id}` | Get service edge node by ID |
| PUT | `/virtualZenNodes/{id}` | Update service edge node |
| DELETE | `/virtualZenNodes/{id}` | Delete service edge node |
| GET | `/virtualZenClusters` | Get all service edge clusters |
| POST | `/virtualZenClusters` | Add service edge cluster |
| GET | `/virtualZenClusters/{id}` | Get service edge cluster by ID |
| PUT | `/virtualZenClusters/{id}` | Update service edge cluster |
| DELETE | `/virtualZenClusters/{id}` | Delete service edge cluster |

### Shadow IT Report (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shadowIT/applications/export` | Export shadow IT cloud applications report |
| POST | `/shadowIT/applications/USER/exportCsv` | Export users for a cloud application |
| POST | `/shadowIT/applications/LOCATION/exportCsv` | Export locations for a cloud application |

### System Audit Report (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/configAudit` | Get config audit |
| GET | `/configAudit/ipVisibility` | Get config audit IP visibility |
| GET | `/configAudit/pacFile` | Get config audit PAC file |

### SSL Inspection (implied from MCP tools)

SSL inspection rules are managed via MCP tools. The API endpoints follow the standard CRUD pattern under `/sslInspectionRules`.

### Traffic Forwarding (28 endpoints)

#### VPN Credentials

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vpnCredentials` | Get all VPN credentials |
| GET | `/vpnCredentials/{id}` | Get VPN credential by ID |
| POST | `/vpnCredentials` | Add VPN credential |
| PUT | `/vpnCredentials/{id}` | Update VPN credential |
| DELETE | `/vpnCredentials/{id}` | Delete VPN credential |
| POST | `/vpnCredentials/bulkDelete` | Bulk delete VPN credentials |

#### Data Center VIPs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vips` | Get all data center VIPs |
| GET | `/vips/groupByDatacenter` | Get VIPs grouped by data center |

#### GRE Tunnels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/greTunnels` | Get all GRE tunnels |
| GET | `/greTunnels/{id}` | Get GRE tunnel by ID |
| GET | `/vips/recommendedList` | Get recommended VIPs for GRE |
| GET | `/greTunnels/availableInternalIpRanges` | Get available internal GRE IP ranges |
| POST | `/greTunnels` | Add GRE tunnel |
| PUT | `/greTunnels/{id}` | Update GRE tunnel |
| DELETE | `/greTunnels/{id}` | Delete GRE tunnel |

#### Static IPs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/staticIP` | Get all static IPs |
| GET | `/staticIP/{id}` | Get static IP by ID |
| POST | `/staticIP/validate` | Validate static IP |
| POST | `/staticIP` | Add static IP (auto or manual region) |
| PUT | `/staticIP/{id}` | Update static IP |
| DELETE | `/staticIP/{id}` | Delete static IP |

#### Geo Lookup

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/region/search` | Get city geo info by name |
| GET | `/region/byGeoCoordinates` | Get city geo info by coordinates |
| GET | `/region/byIPAddress/{ip}` | Get city geo info by IP address |

#### IPv6

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ipv6config` | Get IPv6 configuration |
| GET | `/ipv6config/nat64prefix` | Get NAT64 prefixes |
| GET | `/ipv6config/dns64prefix` | Get DNS64 prefixes |

### Time Intervals (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/timeIntervals` | Get all time intervals |
| GET | `/timeIntervals/{id}` | Get time interval by ID |
| POST | `/timeIntervals` | Add time interval |
| PUT | `/timeIntervals/{id}` | Update time interval |
| DELETE | `/timeIntervals/{id}` | Delete time interval |

### Traffic Capture Policy (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/trafficCaptureRules` | Get all traffic capture rules |
| GET | `/trafficCaptureRules/{id}` | Get traffic capture rule by ID |
| POST | `/trafficCaptureRules` | Add traffic capture rule |
| PUT | `/trafficCaptureRules/{id}` | Update traffic capture rule |
| DELETE | `/trafficCaptureRules/{id}` | Delete traffic capture rule |
| GET | `/trafficCaptureRules/count` | Get rule count |
| GET | `/trafficCaptureRules/order` | Get rule order |
| GET | `/trafficCaptureRules/ruleLabels` | Get rule labels for capture rules |

### URL Categories (11 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/urlCategories` | Get all URL categories (or custom only) |
| GET | `/urlCategories/lite` | Get all URL categories (lite) |
| GET | `/urlCategories/{id}` | Get URL category by ID |
| GET | `/urlCategories/urlQuota` | Get URL quota |
| POST | `/urlCategories` | Add custom URL category |
| PUT | `/urlCategories/{id}` | Update URL category (add/remove URLs) |
| DELETE | `/urlCategories/{id}` | Delete custom URL category |
| POST | `/urlLookup` | Lookup URL categorization |

### URL Filtering Policies (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/urlFilteringRules` | Get all URL filtering rules |
| GET | `/urlFilteringRules/{id}` | Get URL filtering rule by ID |
| POST | `/urlFilteringRules` | Add URL filtering rule |
| PUT | `/urlFilteringRules/{id}` | Update URL filtering rule |
| DELETE | `/urlFilteringRules/{id}` | Delete URL filtering rule |

### URL Filter & Cloud App Settings (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/advancedUrlFilterAndCloudAppSettings` | Get URL filter and cloud app settings |
| PUT | `/advancedUrlFilterAndCloudAppSettings` | Update URL filter and cloud app settings |

### User Authentication Settings (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authSettings/exemptedUrls` | Get auth bypass URLs |
| POST | `/authSettings/exemptedUrls` | Add/Remove URLs from auth bypass list |

### User Management (23 endpoints)

#### Departments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/departments` | Get all departments |
| GET | `/departments/lite` | Get all departments (lite) |
| GET | `/departments/{id}` | Get department by ID |
| POST | `/departments` | Add department |
| PUT | `/departments/{id}` | Update department |
| DELETE | `/departments/{id}` | Delete department |

#### Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/groups` | Get all groups |
| GET | `/groups/lite` | Get all groups (lite) |
| GET | `/groups/{id}` | Get group by ID |
| POST | `/groups` | Add group |
| PUT | `/groups/{id}` | Update group |
| DELETE | `/groups/{id}` | Delete group |

#### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Get all users (supports search by group, name, department) |
| GET | `/users/{id}` | Get user by ID |
| GET | `/users/references` | Get all user references |
| GET | `/users/auditors` | Get all auditors |
| POST | `/users` | Add user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |
| POST | `/users/bulkDelete` | Bulk delete users |

### Workload Groups (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workloadGroups` | Get all workload groups |
| GET | `/workloadGroups/{id}` | Get workload group by ID |
| POST | `/workloadGroups` | Add workload group |
| PUT | `/workloadGroups/{id}` | Update workload group |
| DELETE | `/workloadGroups/{id}` | Delete workload group |

