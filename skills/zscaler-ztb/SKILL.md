---
name: zscaler-ztb
description: Use when working with ZTB (Zero Trust Branch) — AirGap API for sites, gateways, VLANs, PBR, VRRP, IPsec, GRE, WireGuard, IPAM, SNMP, device posture, remote isolation, BGP, OSPF, templates, integrations.
---

# Zero Trust Branch (ZTB)

## Overview

ZTB manages branch office connectivity via Zscaler Branch Connectors. Uses the AirGap API (NOT OneAPI). No MCP tools available -- all operations require direct HTTP calls via Python urllib or curl.

## MCP Tools

No MCP tools. All ZTB operations use the AirGap API directly.

## Authentication

Same Zscaler OneAPI OAuth2 token (client_credentials grant):

```python
import urllib.request, urllib.parse, json, ssl

env = {}
with open(".env") as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k] = v

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

token_data = urllib.parse.urlencode({
    "client_id": env["ZSCALER_CLIENT_ID"],
    "client_secret": env["ZSCALER_CLIENT_SECRET"],
    "grant_type": "client_credentials"
}).encode()
req = urllib.request.Request("https://<vanity>.zslogin.net/oauth2/v1/token", data=token_data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
token = json.loads(urllib.request.urlopen(req, context=ctx).read())["access_token"]

# AirGap API call
req = urllib.request.Request("https://<site-name>-api.goairgap.com/api/v2/<endpoint>")
req.add_header("Authorization", f"Bearer {token}")
result = json.loads(urllib.request.urlopen(req, context=ctx).read())
```

| Property | Value |
|----------|-------|
| **Base URL** | `https://<site-name>-api.goairgap.com` |
| **Web UI** | `https://<site-name>.goairgap.com` |
| **Auth** | Same Zscaler OneAPI OAuth2 token (client_credentials) |
| **API versions** | v2 and v3 (NOT v1) |

---

## API Reference (674 endpoints)

### Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/logs` | Get data for visibility chart |

### v2 Endpoints

#### Application Gateway

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/ApplicationGateway` | Get all application gateways |
| POST | `/api/v2/ApplicationGateway` | Create application gateway |
| GET | `/api/v2/ApplicationGateway/connections/{access_gateway_id}` | Get application gateway by access gateway id |
| DELETE | `/api/v2/ApplicationGateway/{gateway_id}` | Delete application gateway |
| GET | `/api/v2/ApplicationGateway/{gateway_id}` | Get application gateway by id |
| PUT | `/api/v2/ApplicationGateway/{gateway_id}` | Update application gateway |

#### Certificate Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/CertificateProfiles` | Get all certificate profiles |
| POST | `/api/v2/CertificateProfiles` | Create certificate profile |
| GET | `/api/v2/CertificateProfiles/SiteList` | Get all certificate profiles site list |
| POST | `/api/v2/CertificateProfiles/activateOrDeactivate/{id}` | Activate or deactivate certificate profile |
| POST | `/api/v2/CertificateProfiles/validateCertificate` | Validate SSL certificate |
| POST | `/api/v2/CertificateProfiles/validatePrivateKey` | Validate private key |
| DELETE | `/api/v2/CertificateProfiles/{id}` | Delete certificate profile |
| GET | `/api/v2/CertificateProfiles/{id}` | Get certificate profile by id |
| PUT | `/api/v2/CertificateProfiles/{id}` | Update certificate profile |

#### Cloud Gateway

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/CloudGateway/id/{gatewayId}` | Get cloud gateway by ID |
| GET | `/api/v2/CloudGateway/regions/{provider}` | Get regions for cloud gateway deployment |

#### Sites

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/Site/` | List all sites |
| POST | `/api/v2/Site/` | Create site |
| GET | `/api/v2/Site/siteByID/{id}` | Get site by ID |
| GET | `/api/v2/Site/siteByID/{id}/overview` | Site overview data |
| GET | `/api/v2/Site/siteByName/{name}` | Get site by name |
| GET | `/api/v2/Site/names` | All site names |
| GET | `/api/v2/Site/MD5` | Get gateway MD5 |
| GET | `/api/v2/Site/app_segments` | Get ZPA app segments |
| POST | `/api/v2/Site/app_segments/{site_id}` | Update ZPA app segments for site |
| GET | `/api/v2/Site/hostnameconfig` | Get hostname config |
| POST | `/api/v2/Site/cloudSite/` | Create cloud gateway site |
| PUT | `/api/v2/Site/{id}` | Update site |
| PUT | `/api/v2/Site/{id}/template/{template_id}` | Update site template |
| PUT | `/api/v2/Site/{id}/static_ips_mapping` | Update app segments static IPs mapping for site |
| DELETE | `/api/v2/Site/{siteId}` | Delete site |

#### Gateways

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/Gateway/` | List all gateways |
| POST | `/api/v2/Gateway/` | Create gateway |
| GET | `/api/v2/Gateway/id/{gatewayId}` | Get gateway by ID |
| GET | `/api/v2/Gateway/name/{gatewayName}` | Get gateway by name |
| DELETE | `/api/v2/Gateway/id/{gatewayId}` | Delete gateway |
| PATCH | `/api/v2/Gateway/id/{gatewayId}` | Patch update gateway |
| PUT | `/api/v2/Gateway/id/{gatewayId}` | Update gateway |
| PUT | `/api/v2/Gateway/name/{gatewayName}` | Update gateway by name |
| GET | `/api/v2/Gateway/gatewaySettingsById/{id}` | Get gateway settings |
| GET | `/api/v2/Gateway/releases` | Available firmware versions |
| GET | `/api/v2/Gateway/interfaces` | Get all interfaces |
| POST | `/api/v2/Gateway/interfaces` | Create gateway interfaces |
| DELETE | `/api/v2/Gateway/interface/{id}` | Delete gateway interface |
| PUT | `/api/v2/Gateway/interface/{id}` | Update gateway interface |
| POST | `/api/v2/Gateway/upgrade` | Upgrade gateway version |
| POST | `/api/v2/Gateway/rma` | RMA gateway |
| POST | `/api/v2/Gateway/sendactivationlink` | Send activation URL |
| POST | `/api/v2/Gateway/validateActivationCode` | Validate activation code |
| POST | `/api/v2/Gateway/sw_image_update/id/{gatewayId}` | Update software image version |
| PUT | `/api/v2/Gateway/updateVirtualIP/{clusterid}` | Update virtual IP |
| PUT | `/api/v2/Gateway/updateVrrpState/{id}` | Update VRRP state |
| GET | `/api/v2/ClusterGateway/get` | Get gateways by site and cluster name |

#### Cluster

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/cluster/clusterByName/get` | Get cluster by name |
| PUT | `/api/v2/cluster/{cluster_id}` | Update cluster |
| GET | `/api/v2/cluster/{cluster_id}/gatewayType` | Get gateway type |
| GET | `/api/v2/cluster/{cluster_id}/lastUpdatedTime` | Get last updated time |
| PUT | `/api/v2/cluster/{cluster_id}/secure-dns` | Update secure DNS config |
| PUT | `/api/v2/cluster/{cluster_id}/user-reachable-ip` | Update user reachable IP |
| POST | `/api/v2/cluster/initiateSwitchover` | HA switchover |
| POST | `/api/v2/cluster/upgrade` | Upgrade cluster |
| POST | `/api/v2/cluster/download` | Start download |
| POST | `/api/v2/cluster/restore` | Start restore |
| POST | `/api/v2/cluster/execute-cmd` | Execute debug command |
| POST | `/api/v2/cluster/cmd-response` | Post debug command response |
| POST | `/api/v2/cluster/set-debug-status/{cluster_id}` | Set debug on/off |
| POST | `/api/v2/cluster/initiate-endpoint-discovery` | Start endpoint discovery |
| POST | `/api/v2/cluster/protectedsubnets` | Configure protected subnets |
| POST | `/api/v2/cluster/bulk-update-tenants-releases` | Bulk update gateway releases |

#### Cluster -- IPsec

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/cluster/ipsec-config` | Get IPsec config |
| POST | `/api/v2/cluster/ipsec-config` | Configure IPsec |
| PUT | `/api/v2/cluster/ipsec-config` | Update IPsec |
| DELETE | `/api/v2/cluster/ipsec-config` | Delete IPsec config |
| GET | `/api/v2/cluster/ipsec-config/lastupdatedtime` | IPsec config last updated time |
| POST | `/api/v2/cluster/ipsec-config/remoteaddr` | Post IPsec peer addresses |
| GET | `/api/v2/cluster/ipsec-status` | Get tunnel status |
| POST | `/api/v2/cluster/ipsec-status` | Post tunnel status |

#### Cluster -- DHCP & NTP

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/cluster/dhcp-options/{cluster_id}` | Add DHCP option |
| PUT | `/api/v2/cluster/dhcp-options/{cluster_id}/{index}` | Update DHCP option |
| DELETE | `/api/v2/cluster/dhcp-options/{cluster_id}/{index}` | Delete DHCP option |
| GET | `/api/v2/cluster/standard/dhcp-options` | Get standard DHCP options and types |
| GET | `/api/v2/cluster/ntp-servers/{cluster_id}` | Get NTP server config |
| POST | `/api/v2/cluster/ntp-servers` | Modify NTP server config |

#### Cluster -- SNMP

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/cluster/{cluster_id}/snmp-profile` | Get SNMP profile for cluster |
| POST | `/api/v2/cluster/{cluster_id}/snmp-profile` | Create SNMP profile |
| PUT | `/api/v2/cluster/{cluster_id}/snmp-profile` | Update SNMP profile |

#### Networks (VLANs)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/Network/` | List all networks |
| POST | `/api/v2/Network/` | Create network |
| GET | `/api/v2/Network/get/{network_id}` | Get network by ID |
| GET | `/api/v2/Network/{gateway_id}` | List networks by gateway |
| GET | `/api/v2/Network/networkByName/{gateway_name}/{network_name}` | Get network by name |
| PUT | `/api/v2/Network/update/{network_id}` | Update network |
| DELETE | `/api/v2/Network/delete/{id}` | Delete network |
| PATCH | `/api/v2/Network/enforcement` | Enable/disable enforcement |
| PATCH | `/api/v2/Network/windows_server` | Enable/disable Windows server |
| POST | `/api/v2/Network/state-transition/next/{network_id}` | Advance state |
| POST | `/api/v2/Network/state-transition/cancel/{network_id}` | Cancel state transition |
| POST | `/api/v2/Network/check-display-name` | Check display name |
| POST | `/api/v2/Network/default-gateway` | Calculate default gateway by IP range |
| GET | `/api/v2/Network/ip-range-validation` | IP range validation |
| GET | `/api/v2/Network/vlan-validation` | VLAN tag validation |
| POST | `/api/v2/Network/validate-ip` | Validate IPs |
| POST | `/api/v2/Network/uplink-ip` | Calculate uplink IP |
| GET | `/api/v2/Network/max_devices` | Max number of devices |
| GET | `/api/v2/Network/assignments/{network_id}` | Get scanned devices by network |
| GET | `/api/v2/Network/ip-reservations/{id}` | Get IP reservations by network |
| GET | `/api/v2/Network/reservations/lastUpdatedTime` | IP reservations last updated time |
| POST | `/api/v2/Network/reserveIPByNetwork/{network_id}` | Reserve IP addresses |
| POST | `/api/v2/Network/validateUpload` | Validate network upload |
| POST | `/api/v2/Network/validateUploadByNetwork/{network_id}` | Validate upload by network |
| GET | `/api/v2/NetworkManagement/downloadConfigs` | Download network hub configurations |

#### Alarms

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/alarm` | Get all alarms |
| POST | `/api/v2/alarm` | Create alarm |
| PATCH | `/api/v2/alarm` | Update alarm |
| PUT | `/api/v2/alarm` | Update alarm |
| DELETE | `/api/v2/alarm/{alarmId}` | Delete alarm |
| PATCH | `/api/v2/alarm/bulkAcknowledge` | Bulk acknowledge alarms |
| PATCH | `/api/v2/alarm/bulkAcknowledgeAll` | Acknowledge all active alarms |
| DELETE | `/api/v2/alarm/bulkIgnore` | Bulk ignore alarms |
| DELETE | `/api/v2/alarm/bulkIgnoreAll` | Ignore all active alarms |

#### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/auth/login` | User authentication |
| POST | `/api/v2/auth/logout` | User logout |
| POST | `/api/v2/auth/csp/login` | Login from CSP |
| POST | `/api/v2/auth/sso-login` | SSO login using email |
| POST | `/api/v2/auth/sso-token` | Generate SSO token for OAuth/OpenID |
| GET | `/api/v2/auth/sso/config` | Get SSO config |
| POST | `/api/v2/auth/zid/token` | Authenticate using ZID SSO |
| POST | `/api/v2/auth/zid/logout` | ZID user logout |
| POST | `/api/v2/auth/auth0/token` | Generate SSO token for Auth0 |
| POST | `/api/v2/auth/auth0/logout` | Auth0 user logout |
| GET | `/api/v2/auth/auth0/config` | Get Auth0 config |
| POST | `/api/v2/auth/request-reset-password` | Password reset request |
| POST | `/api/v2/auth/reset-password` | Password reset |
| POST | `/api/v2/auth/verify-reset-code` | Verify reset code |

#### Auth0 Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/auth0/user/users` | Get all Auth0 users |
| POST | `/api/v2/auth0/user/invite` | Invite Auth0 user |
| DELETE | `/api/v2/auth0/user/{id}` | Delete Auth0 user |
| PUT | `/api/v2/auth0/user/{id}` | Update Auth0 user roles |
| PUT | `/api/v2/auth0/user/resendinvite/{id}` | Resend invitation |

#### Customer

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/customer/customers` | Customer config |
| GET | `/api/v2/customer/customers/list` | Customer list |
| POST | `/api/v2/customer/create_customer` | Create customer |
| DELETE | `/api/v2/customer/{id}` | Delete customer |
| PUT | `/api/v2/customer/{id}` | Update customer |
| GET | `/api/v2/customer/search/{tenant}` | Search customer names |
| POST | `/api/v2/customer/delegate/{tenant_customer_id}` | Delegate login |
| POST | `/api/v2/customer/feedback` | Post feedback |
| POST | `/api/v2/customer/support-access` | Allow support access |
| POST | `/api/v2/customer/support-access/request` | Request support access |
| GET | `/api/v2/customer/{tenant}/domains` | Get email domains |
| GET | `/api/v2/customer/{tenant}/roles` | Get tenant roles |
| PUT | `/api/v2/customer/ui/logo/{tenant_id}` | Update customer logo |
| DELETE | `/api/v2/customer/ui/logo/{tenant_id}` | Delete customer logo |
| GET | `/api/v2/Customer/config` | Customer config |
| GET | `/api/v2/Customer/mssp_name` | Customer MSSP name |

#### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/dashboard/cards` | Get dashboard cards |
| GET | `/api/v2/dashboard/cards/{card}` | Get specific dashboard card |
| GET | `/api/v2/dashboard/tiles-info` | Dashboard tiles data |
| GET | `/api/v2/dashboard/site-info` | Sites info with gateway info |
| GET | `/api/v2/dashboard/percentage-change` | Percentage change data |
| GET | `/api/v2/dashboard/red/anomalies` | Ransomware anomalies |
| POST | `/api/v2/dashboard/elasticsearch/bytes-sum` | Elasticsearch bytes sum |
| POST | `/api/v2/dashboard/elasticsearch/latency` | Elasticsearch latency |
| POST | `/api/v2/dashboard/elasticsearch/top-applications` | Top applications |
| POST | `/api/v2/dashboard/elasticsearch/top-countries` | Top countries |
| POST | `/api/v2/dashboard/elasticsearch/top-devices` | Top devices |
| GET | `/api/v2/dashboard/elasticsearch/intra-vlan-data` | Intra-VLAN chart data |
| GET | `/api/v2/dashboard/elasticsearch/intra-vlan-data/protocols` | Intra-VLAN protocols |
| GET | `/api/v2/dashboard/elasticsearch/kibana-link` | Kibana link |
| GET | `/api/v2/dashboard/elasticsearch/user-application-access-chart` | User application access |
| GET | `/api/v2/dashboard/mssp/cards` | MSSP dashboard cards |
| POST | `/api/v2/dashboard/mssp/cards` | MSSP dashboard cards (POST) |
| GET | `/api/v2/dashboard/mssp/cards/{card}` | Specific MSSP card |
| GET | `/api/v2/dashboard/mssp/tiles` | MSSP tiles |
| POST | `/api/v2/dashboard/mssp/tiles` | MSSP tiles (POST) |
| POST | `/api/v2/dashboard/mssp/policies` | MSSP policies history |
| POST | `/api/v2/dashboard/mssp/policies/bychange` | Policies by change |
| POST | `/api/v2/dashboard/mssp/policies/bytenant` | Policies by tenant |
| POST | `/api/v2/dashboard/mssp/policies/bytime` | Policies by time |

#### Devices

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/devices/active` | Get active devices |
| GET | `/api/v2/devices/active/details/{deviceId}/{minutes}` | Device details |
| GET | `/api/v2/devices/details/id/{deviceId}/{minutes}` | DHCP history |
| GET | `/api/v2/devices/auditlog` | DHCP event list |
| POST | `/api/v2/devices/bulk-update` | Bulk update device assignment/status |
| PATCH | `/api/v2/devices/{id}` | Update device assignment/status |
| GET | `/api/v2/devices/tags` | Get device tags |
| PUT | `/api/v2/devices/tags` | Bulk update device tags |
| PUT | `/api/v2/devices/tags/{id}` | Update tags for device |

#### Device Attributes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/device-attributes` | Get all device attributes |
| POST | `/api/v2/device-attributes` | Create device attribute |
| DELETE | `/api/v2/device-attributes` | Delete all device attributes |
| GET | `/api/v2/device-attributes/collections` | Get attributes for menu |
| GET | `/api/v2/device-attributes/device_ip/{device_ip}` | Get by device IP |
| PUT | `/api/v2/device-attributes/device_ip/{device_ip}` | Update by device IP |
| DELETE | `/api/v2/device-attributes/device_ip/{device_ip}` | Delete by device IP |
| GET | `/api/v2/device-attributes/id/{dev_attr_id}` | Get by attribute ID |
| GET | `/api/v2/device-attributes/operators` | Get operators for security posture |

#### Compromised Devices

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/compromised-device/get/{tab}` | Get compromised devices |
| POST | `/api/v2/compromised-device/insert` | Blacklist insert |
| PATCH | `/api/v2/compromised-device/bulkAcknowledge` | Bulk acknowledge threats |
| PATCH | `/api/v2/compromised-device/bulkAcknowledgeAll` | Acknowledge all active threats |
| DELETE | `/api/v2/compromised-device/bulkIgnore` | Bulk ignore threats |
| DELETE | `/api/v2/compromised-device/bulkIgnoreAll` | Ignore all active threats |

#### DHCP Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/dhcp-events` | Post DHCP event |
| POST | `/api/v2/dhcp-events/bulk` | Bulk DHCP events |

#### Scanned Devices

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/scanned-devices` | Post scanned devices |

#### Group Policies (Segmentation)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/group-policies` | Get all group policies |
| POST | `/api/v2/group-policies` | Create group policy |
| DELETE | `/api/v2/group-policies` | Delete all group policies |
| GET | `/api/v2/group-policies/{policy_id}` | Get policy by ID |
| PUT | `/api/v2/group-policies/{policy_id}` | Update policy by ID |
| DELETE | `/api/v2/group-policies/{policy_id}` | Delete policy by ID |
| GET | `/api/v2/group-policies/name/{policy_name}` | Get policy by name |
| PUT | `/api/v2/group-policies/name/{policy_name}` | Update policy by name |
| DELETE | `/api/v2/group-policies/name/{policy_name}` | Delete policy by name |
| POST | `/api/v2/group-policies/bulk` | Bulk create policies |
| PUT | `/api/v2/group-policies/bulk` | Bulk update policies |
| DELETE | `/api/v2/group-policies/bulk` | Bulk delete policies |
| POST | `/api/v2/group-policies/resequence` | Resequence policies |
| POST | `/api/v2/group-policies/import` | Import policies |
| POST | `/api/v2/group-policies/validateimport` | Validate import |
| GET | `/api/v2/group-policies/policychecker` | Check policies |
| GET | `/api/v2/group-policies/populate` | Get protocol:port pairs |
| POST | `/api/v2/group-policies/removeunusedgroups` | Remove unused private groups |
| GET | `/api/v2/group-policies/device-protection/policies` | Get device protection policies |
| POST | `/api/v2/group-policies/device-protection/policies` | Create device protection policies |
| GET | `/api/v2/group-policies/{site-id}/hitcount` | Get hit counters |
| POST | `/api/v2/group-policies/{site-id}/clearhitcount` | Clear hit counters |

#### Group Policy Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/group-policy-rules` | Get all policy rules |
| POST | `/api/v2/group-policy-rules` | Create policy rule |
| DELETE | `/api/v2/group-policy-rules` | Delete all policy rules |
| GET | `/api/v2/group-policy-rules/{rule_id}` | Get rule by ID |
| PUT | `/api/v2/group-policy-rules/{rule_id}` | Update rule by ID |
| DELETE | `/api/v2/group-policy-rules/{rule_id}` | Delete rule by ID |
| GET | `/api/v2/group-policy-rules/last-update-time` | Last update time |

#### Groups (Membership)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/groups` | Get all groups |
| POST | `/api/v2/groups` | Create group |
| DELETE | `/api/v2/groups` | Delete all groups |
| GET | `/api/v2/groups/{group_id}` | Get group by ID |
| PUT | `/api/v2/groups/{group_id}` | Update group |
| PATCH | `/api/v2/groups/{group_id}` | Patch group |
| DELETE | `/api/v2/groups/{group_id}` | Delete group |
| GET | `/api/v2/groups/name/{group_name}` | Get group by name |
| PUT | `/api/v2/groups/name/{group_name}` | Update group by name |
| DELETE | `/api/v2/groups/name/{group_name}` | Delete group by name |
| GET | `/api/v2/groups/policylist/name/{group_name}` | Get policies using group |
| GET | `/api/v2/groups/policylist/{group_id}` | Get policies using group (by ID) |
| GET | `/api/v2/groups/applications` | Get applications for app groups |
| GET | `/api/v2/groups/application-groups/{applicationId}` | Get access app groups |
| GET | `/api/v2/groups/user-groups/{userId}` | Get user groups |
| GET | `/api/v2/groups/tcpudpports` | Get TCP/UDP ports |
| GET | `/api/v2/groups/saas-apps` | Get SaaS apps predefined list |
| PUT | `/api/v2/groups/quarantine-mac` | Add/remove MAC from quarantine group |
| POST | `/api/v2/groups/sync-memberships` | Sync group memberships |
| POST | `/api/v2/groups/shadow-groups` | Get shadow groups |
| GET | `/api/v2/groups/crowdstrike` | Get CrowdStrike groups |
| POST | `/api/v2/groups/crowdstrike/sync` | Sync CrowdStrike groups |
| GET | `/api/v2/groups/oidc-groups` | Get OIDC groups |
| POST | `/api/v2/groups/oidc-groups/sync` | Sync OIDC groups |

#### Group Membership

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/group-membership` | Get group membership |
| PUT | `/api/v2/group-membership` | Update group membership |
| GET | `/api/v2/group-membership/groups` | Get groups matching IP prefix |
| GET | `/api/v2/group-membership/last-update-time` | Last update time |

#### Integrations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v2/integrations/partner/` | Create partner entry |
| GET | `/api/v2/integrations/partner/{partnerName}` | Get partner details |
| POST | `/api/v2/integrations/partner/{partnerName}/test` | Test partner API token |
| GET | `/api/v2/integrations/invoke/{partnerName}/{apiName}` | Invoke partner API |
| GET | `/api/v2/integrations/token/` | Get partner auth token |
| POST | `/api/v2/integrations/sync/{partnerName}` | Sync device info from partner |
| GET | `/api/v2/integrations/sync/{partnerName}` | Sync all devices with partner |
| POST | `/api/v2/integrations/sync/zscaler-services` | Sync Zscaler services (ZIA/ZPA) |
| PUT | `/api/v2/integrations/settings/sso-config` | Update SSO config |
| PUT | `/api/v2/integrations/settings/siem-integration` | Update SIEM integration |
| PUT | `/api/v2/integrations/settings/ad-integration` | Update AD integration |
| PUT | `/api/v2/integrations/settings/non-web-oidc` | Update non-web OIDC |
| PUT | `/api/v2/integrations/settings/reset-kibana-credentials` | Reset Kibana credentials |
| GET | `/api/v2/integrations/settings/remote-isolation/{type}` | Get remote isolation settings |
| POST | `/api/v2/integrations/settings/remote-isolation/{type}` | Save remote isolation settings |
| POST | `/api/v2/integrations/settings/remote-isolation/{type}/test` | Test remote isolation settings |
| PUT | `/api/v2/integrations/global/private-dns-servers` | Update private DNS servers |

#### IPAM

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/ipam/fetchGroups` | Get IPAM group list |
| POST | `/api/v2/ipam/createGroup` | Create IPAM group |
| PUT | `/api/v2/ipam/updateGroup` | Update IPAM group |
| DELETE | `/api/v2/ipam/deleteGroup` | Delete IPAM group |
| POST | `/api/v2/ipam/createSubGroup` | Create IPAM sub group |
| PUT | `/api/v2/ipam/updateSubGroup` | Update IPAM sub group |
| DELETE | `/api/v2/ipam/deleteSubGroup` | Delete IPAM sub group |
| POST | `/api/v2/ipam/subnet` | Create subnet |
| GET | `/api/v2/ipam/subnetGroups` | Get subnet group list |
| GET | `/api/v2/ipam/subGroupSubNetList/{group_id}/{subgroup_id}` | Get sub group subnet list |
| GET | `/api/v2/ipam/subnetIPList/{group_id}/{subnet}` | Get subnet IP list |
| GET | `/api/v2/ipam/subnetIPList/{group_id}/{subnet}/{subgroup_id}` | Get subnet IP list (with sub group) |
| GET | `/api/v2/ipam/topSubnetUtilization` | Top subnet utilization |
| GET | `/api/v2/ipam/getIpDetail/{ip_address}` | Get IP detail |
| POST | `/api/v2/ipam/saveIpDetail` | Save IP detail |
| POST | `/api/v2/ipam/dhcpAddSubnet` | DHCP add subnet |
| POST | `/api/v2/ipam/dhcpLease` | DHCP lease |

#### SNMP

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/snmp/group` | Get SNMP security groups |
| POST | `/api/v2/snmp/group` | Create SNMP group |
| PATCH | `/api/v2/snmp/group` | Update SNMP group |
| DELETE | `/api/v2/snmp/group` | Delete SNMP group |
| GET | `/api/v2/snmp/profile` | Get SNMP profiles |
| POST | `/api/v2/snmp/profile` | Create SNMP profile |
| PATCH | `/api/v2/snmp/profile` | Update SNMP profile |
| DELETE | `/api/v2/snmp/profile` | Delete SNMP profile |
| GET | `/api/v2/snmp/profiledata` | Get SNMP profile data |
| POST | `/api/v2/snmp/profile/assign` | Assign SNMP profile |
| DELETE | `/api/v2/snmp/profile/assign` | Remove SNMP profile assignment |
| POST | `/api/v2/snmp/profile/assigngroup` | Assign security group to profile |
| GET | `/api/v2/snmp/profile/assigngroup` | Get profiles assigned to group |
| DELETE | `/api/v2/snmp/profile/assigngroup` | Remove security group from profile |
| POST | `/api/v2/snmp/profile/assigntrap` | Assign trap to profile |
| GET | `/api/v2/snmp/trap` | Get SNMP traps |
| POST | `/api/v2/snmp/trap` | Create SNMP trap |
| PATCH | `/api/v2/snmp/trap` | Update SNMP trap |
| DELETE | `/api/v2/snmp/trap` | Delete SNMP trap |
| GET | `/api/v2/snmp/user` | Get SNMP users |
| POST | `/api/v2/snmp/user` | Create SNMP user |
| PATCH | `/api/v2/snmp/user` | Update SNMP user |
| DELETE | `/api/v2/snmp/user` | Delete SNMP user |
| GET | `/api/v2/snmp/view` | Get SNMP views |
| POST | `/api/v2/snmp/view` | Create SNMP view |
| PATCH | `/api/v2/snmp/view` | Update SNMP view |
| DELETE | `/api/v2/snmp/view` | Delete SNMP view |

#### Disposable Jump Box

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/dispjumpbox/active/` | Get active jump boxes for user |
| POST | `/api/v2/dispjumpbox/vm/` | Create disposable jump box |
| DELETE | `/api/v2/dispjumpbox/vm/{id}` | Delete jump box |
| GET | `/api/v2/dispjumpbox/rdp/` | Get RDP file for application |
| GET | `/api/v2/dispjumpbox/amiversions` | Get AMI versions |
| POST | `/api/v2/dispjumpbox/amiversions` | Add AMI version |
| GET | `/api/v2/dispjumpbox/djb-allowed-address` | Get allowed IP list |
| POST | `/api/v2/dispjumpbox/djb-allowed-address` | Update allowed IP list |
| GET | `/api/v2/dispjumpbox/djb-allowed-dns` | Get allowed DNS list |
| POST | `/api/v2/dispjumpbox/djb-allowed-dns` | Update allowed DNS list |
| POST | `/api/v2/dispjumpbox/idle` | Process idle time |
| GET | `/api/v2/dispjumpbox/ip` | Get user for IP |
| GET | `/api/v2/dispjumpbox/listrecordings` | List jump box recordings |
| POST | `/api/v2/dispjumpbox/recordings` | Get recording URLs |

#### Users & Roles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/user/users` | Get all users |
| POST | `/api/v2/user/user` | Create user |
| PUT | `/api/v2/user/user` | Update user |
| DELETE | `/api/v2/user/user/{id}` | Delete user |
| GET | `/api/v2/user/profile` | Get user profile |
| GET | `/api/v2/user/profile/permissions` | Get user permissions |
| PUT | `/api/v2/user/{id}` | Update user profile |
| PUT | `/api/v2/user/password` | Change password |
| GET | `/api/v2/user/roles` | Get all roles |
| GET | `/api/v2/user/refreshtoken` | Get refresh token |
| POST | `/api/v2/user/switch_profile/{type}` | Switch user profile |
| POST | `/api/v2/user/admin/sync` | Sync admin users from OIDC |

#### Store (State Persistence)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/store/namespaces` | List store namespaces |
| GET | `/api/v2/store/state/{namespace}/{scope}` | Get user state |
| PUT | `/api/v2/store/state/{namespace}/{scope}` | Update user state |
| GET | `/api/v2/store/state/{namespace}/{scope}/default` | Get default state |
| PUT | `/api/v2/store/state/{namespace}/{scope}/default` | Update default state |

#### Backend

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/backend/version` | Get backend version |
| GET | `/api/v2/backend/database/version` | Get database version |
| PUT | `/api/v2/backend/database/version` | Upgrade database version |
| GET | `/api/v2/backend/database/version-check` | Check database version mismatch |

#### User Entities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/user-entities/get-count` | Get entity count |

### v3 Endpoints

#### BGP

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/Bgp/` | List BGP peers |
| GET | `/api/v3/Bgp/config/{cluster_id}` | Get BGP peer config |
| POST | `/api/v3/Bgp/config` | Add BGP peer config |
| PUT | `/api/v3/Bgp/config` | Update BGP peer config |
| DELETE | `/api/v3/Bgp/config/{cluster_id}` | Delete BGP peer config |
| DELETE | `/api/v3/Bgp/{bgp_id}` | Delete BGP peer config (by ID) |
| GET | `/api/v3/Bgp/bgpstatus/{cluster_id}` | Get BGP status |
| POST | `/api/v3/Bgp/bgpstatus` | Post BGP status |
| POST | `/api/v3/Bgp/bgpstatusall` | Post BGP status for all peers (legacy) |
| POST | `/api/v3/Bgp/bgpstatusallv2` | Post BGP status for all peers (v2) |
| GET | `/api/v3/Bgp/s2s_bgp_status/{cluster_id}` | Get S2S BGP status |

#### Cloud Gateway (v3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/CloudGateway/hubs` | Get cloud gateways list |
| GET | `/api/v3/CloudGateway/s2s_hubs` | Get S2S VPN hub list |
| GET | `/api/v3/CloudGateway/s2s/{cluster_id}` | Get S2S VPN connections |
| POST | `/api/v3/CloudGateway/s2s/{cluster_id}` | Create S2S VPN connections |
| PUT | `/api/v3/CloudGateway/s2s/{cluster_id}` | Update S2S VPN connections |
| DELETE | `/api/v3/CloudGateway/s2s/{cluster_id}` | Delete S2S VPN connections |
| GET | `/api/v3/CloudGateway/s2s/{cluster_id}/gateways` | Get cluster gateways with interfaces |

#### Gateway (v3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/Gateway/` | List gateways grouped by site/cluster |
| GET | `/api/v3/Gateway/id/{gatewayId}` | Get gateway by ID (v3) |
| GET | `/api/v3/Gateway/name/{gatewayName}` | Get gateway by name (v3) |
| POST | `/api/v3/Gateway/zpa-provision` | Provision ZPA cert |
| POST | `/api/v3/Gateway/zpa-provision/ack` | Acknowledge ZPA cert provision |

#### LLDP

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/Lldp/` | List LLDP peers |
| GET | `/api/v3/Lldp/config/{cluster_id}` | Get LLDP config |
| POST | `/api/v3/Lldp/config` | Add LLDP config |
| PUT | `/api/v3/Lldp/config` | Update LLDP config |
| DELETE | `/api/v3/Lldp/config/{cluster_id}` | Delete LLDP config |
| DELETE | `/api/v3/Lldp/{lldp_id}` | Delete LLDP config (by ID) |

#### OSPF

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/Ospf/` | List OSPF peers |
| GET | `/api/v3/Ospf/config/{cluster_id}` | Get OSPF config |
| POST | `/api/v3/Ospf/config` | Add OSPF config |
| PUT | `/api/v3/Ospf/config` | Update OSPF config |
| DELETE | `/api/v3/Ospf/config/{cluster_id}` | Delete OSPF config |
| DELETE | `/api/v3/Ospf/{ospf_id}` | Delete OSPF config (by ID) |

#### PIM (Protocol Independent Multicast)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/Pim/` | List PIM peers |
| GET | `/api/v3/Pim/config/{cluster_id}` | Get PIM config |
| POST | `/api/v3/Pim/config` | Add PIM config |
| PUT | `/api/v3/Pim/config` | Update PIM config |
| DELETE | `/api/v3/Pim/config/{cluster_id}` | Delete PIM config |
| DELETE | `/api/v3/Pim/{pim_id}` | Delete PIM config (by ID) |

#### Static Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/Staticroute/` | List static routes |
| POST | `/api/v3/Staticroute/config` | Add static route |
| PUT | `/api/v3/Staticroute/config` | Update static route |
| DELETE | `/api/v3/Staticroute/config/{cluster_id}` | Delete static route |
| PATCH | `/api/v3/Staticroute/config/{route_id}/share-over-rt` | Update share-over-RT property |
| DELETE | `/api/v3/Staticroute/{Staticroute_id}` | Delete static route (by ID) |

#### PBR (Policy-Based Routing)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/pbr/policies` | Get PBR policies (requires `?gateway_id=`) |
| POST | `/api/v3/pbr/policies` | Create PBR policy |
| PUT | `/api/v3/pbr/policies` | Update PBR policy |
| DELETE | `/api/v3/pbr/policies` | Delete PBR policy by ID |
| GET | `/api/v3/pbr/policies/{name}` | Get PBR policy by name |
| DELETE | `/api/v3/pbr/policies/{name}` | Delete PBR policy by name |
| POST | `/api/v3/pbr/policies-reorder` | Reorder PBR policies |
| GET | `/api/v3/pbr/interfaces` | Get PBR interfaces (requires `?gateway_id=`) |
| GET | `/api/v3/pbr/rules` | Get PBR rules |
| GET | `/api/v3/pbr/rules/lastupdated` | PBR rules last updated time |
| GET | `/api/v3/pbr/settings` | Get PBR global settings |
| POST | `/api/v3/pbr/settings` | Update PBR global settings |
| POST | `/api/v3/pbr/iptoint-map` | Update interface details in PBR rules |
| GET | `/api/v3/pbr/interface-monitoring` | Get interface monitoring config |
| POST | `/api/v3/pbr/interface-monitoring` | Add interface monitoring config |
| PUT | `/api/v3/pbr/interface-monitoring` | Update interface monitoring config |
| DELETE | `/api/v3/pbr/interface-monitoring` | Delete interface monitoring config |
| GET | `/api/v3/pbr/interface-monitoring/lastupdated` | Interface monitoring last updated |
| POST | `/api/v3/pbr/interface-monitoring/status` | Interface monitoring status |

#### VRRP (HA)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/vrrp/config/{cluster_id}` | Get VRRP config |
| POST | `/api/v3/vrrp/config/{cluster_id}` | Update VRRP config |
| DELETE | `/api/v3/vrrp/config/{cluster_id}` | Delete VRRP config |
| GET | `/api/v3/vrrp/vrrpstatus/{cluster_id}` | Get VRRP status |
| POST | `/api/v3/vrrp/vrrpstatus` | Update VRRP status |
| POST | `/api/v3/vrrp/initiateFailOpen/{cluster_id}` | Initiate fail-open |

#### VRF

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/vrf/config` | Get VRF config |
| POST | `/api/v3/vrf/config` | Add VRF config |
| PUT | `/api/v3/vrf/config` | Update VRF config |
| DELETE | `/api/v3/vrf/config` | Delete VRF config |
| DELETE | `/api/v3/vrf/{vrf_id}` | Delete VRF config (by ID) |

#### GRE Tunnels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/gre/all-tunnels` | List all GRE tunnels |
| GET | `/api/v3/gre/config` | Get GRE config |
| POST | `/api/v3/gre/config` | Configure GRE |
| PUT | `/api/v3/gre/config` | Update GRE |
| DELETE | `/api/v3/gre/config` | Delete GRE config |
| GET | `/api/v3/gre/configbygwid` | Get GRE config by gateway ID |
| GET | `/api/v3/gre/general-gre` | Get general GRE info |
| POST | `/api/v3/gre/general-gre` | Add general GRE tunnel |
| PUT | `/api/v3/gre/general-gre` | Update general GRE tunnel |
| DELETE | `/api/v3/gre/general-gre` | Delete general GRE tunnel |
| GET | `/api/v3/gre/lastupdatedtime` | GRE config last updated time |
| GET | `/api/v3/gre/tunnel-status` | Get GRE tunnel status |
| POST | `/api/v3/gre/tunnel-status` | Post GRE tunnel status |
| GET | `/api/v3/gre/waninterfaces` | Get GRE WAN interfaces |

#### WireGuard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/wireguard/sites` | Get WireGuard sites |
| GET | `/api/v3/wireguard/clients/{cluster_id}` | Get clients by cluster |
| POST | `/api/v3/wireguard/clients/signout` | Client signout |
| GET | `/api/v3/wireguard/clienttunnels/status` | Client tunnel status |
| GET | `/api/v3/wireguard/connectors/{cluster_id}` | Get connectors by cluster |
| GET | `/api/v3/wireguard/connectortunnels/status` | Connector tunnel status |
| POST | `/api/v3/wireguard/tunnels/status` | Post tunnel status |
| GET | `/api/v3/wireguard/config/client` | Get client WireGuard config |
| GET | `/api/v3/wireguard/config/gateway` | Get gateway WireGuard config |
| GET | `/api/v3/wireguard/s2svpn/spoke-overlay-endpoints` | Get S2S VPN spoke overlay endpoints |

#### Devices (v3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/device` | Get devices by category/type |
| POST | `/api/v3/device` | Create NSG devices |
| PATCH | `/api/v3/device` | Bulk update device attributes |
| DELETE | `/api/v3/device` | Bulk delete devices |
| GET | `/api/v3/device/details/{device_id}` | Get device details |
| POST | `/api/v3/device/details/{device_id}` | Set device details |
| GET | `/api/v3/device/{group}` | Get devices by group |
| GET | `/api/v3/device/group-by/{field}` | Get top N devices by field |
| GET | `/api/v3/device/group-by/list` | List group names for graphs |
| GET | `/api/v3/device/filters/{field}/values` | Get filter values by field |
| GET | `/api/v3/device/operating-systems` | Get OS list with device counts |
| POST | `/api/v3/device/upload/assets-csv` | Upload assets CSV |
| POST | `/api/v3/device/validate/assets-csv` | Validate assets CSV |

#### Device Posture

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/deviceposture/profiles` | Get posture profiles |
| POST | `/api/v3/deviceposture/profiles` | Create posture profile |
| PUT | `/api/v3/deviceposture/profiles/{profile_name}` | Update posture profile |
| DELETE | `/api/v3/deviceposture/profiles/{profile_name}` | Delete posture profile |
| GET | `/api/v3/deviceposture/rules` | Get posture rules |
| GET | `/api/v3/deviceposture/config/{os_type}` | Get posture config by OS |
| POST | `/api/v3/deviceposture/currentstatus` | Current posture status |

#### App Connectors (embedded ZPA)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/appconnector/config` | Get app connector config |
| POST | `/api/v3/appconnector/config` | Add app connector config |
| DELETE | `/api/v3/appconnector/config` | Delete app connector config |
| DELETE | `/api/v3/appconnector/{appconnector_id}` | Delete app connector by ID |
| GET | `/api/v3/connector/all` | Get all connectors |
| GET | `/api/v3/connector/{connector_id}` | Get connector by ID |
| PUT | `/api/v3/connector/{connector_id}` | Update connector |
| DELETE | `/api/v3/connector/{connector_id}` | Delete connector |
| POST | `/api/v3/connector` | Create connector |

#### Network (v3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/Network/exportDevices/{network_id}` | Export scanned devices by network |

#### Remote Isolation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/remote-isolation/policies` | Get isolation policies |
| POST | `/api/v3/remote-isolation/policies` | Create isolation policy |
| PUT | `/api/v3/remote-isolation/policies/{policy_id}` | Update isolation policy |
| DELETE | `/api/v3/remote-isolation/policies` | Delete isolation policies |
| GET | `/api/v3/remote-isolation/devices` | Get isolated devices |
| GET | `/api/v3/remote-isolation/services` | Get services (device protection risks) |
| POST | `/api/v3/remote-isolation/services` | Create service |
| GET | `/api/v3/remote-isolation/services/{policy_id}` | Get services per policy |
| POST | `/api/v3/remote-isolation/flows/{policy_id}` | Get flows |
| GET | `/api/v3/remote-isolation/settings/{type}` | Get isolation settings |
| POST | `/api/v3/remote-isolation/settings/{type}` | Save isolation settings |
| POST | `/api/v3/remote-isolation/settings/{type}/test` | Test isolation settings |
| POST | `/api/v3/remote-isolation/signup` | Self-signup |

#### Network Isolation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/network-isolation/counters/{policy_id}` | Get counters per policy |
| POST | `/api/v3/network-isolation/flows/{policy_id}` | Get flows |

#### Ransomware Kill

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/ransomware-kill/state/` | Get ransomware kill state |
| PUT | `/api/v3/ransomware-kill/state/{site_id}/{color}` | Update ransomware kill state |
| GET | `/api/v3/ransomware-kill/email-template/{site_id}` | Get ransomware email template |
| POST | `/api/v3/ransomware-kill/email-template/{site_id}` | Save email template |

#### Browser Protection

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/browser-protection/settings` | Get browser protection settings |
| POST | `/api/v3/browser-protection/settings` | Create browser protection settings |
| PUT | `/api/v3/browser-protection/settings` | Update browser protection settings |
| GET | `/api/v3/browser-protection/safe-extensions` | Get safe extensions |
| POST | `/api/v3/browser-protection/safe-extensions` | Create safe extension |
| PUT | `/api/v3/browser-protection/safe-extensions/{id}` | Update safe extension |
| DELETE | `/api/v3/browser-protection/safe-extensions/{id}` | Delete safe extension |

#### NAC Lite

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/nac-lite/get` | Get NAC MAC list |
| POST | `/api/v3/nac-lite/validate` | Validate NAC MAC CSV |
| POST | `/api/v3/nac-lite/upload` | Upload NAC MAC entries |
| DELETE | `/api/v3/nac-lite/delete` | Delete NAC MAC entries |
| DELETE | `/api/v3/nac-lite/delete/all` | Delete all NAC MAC entries |
| GET | `/api/v3/nac-lite/template` | Get CSV template |

#### Microsoft AD

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v3/microsoftad` | Create Microsoft AD config |
| POST | `/api/v3/microsoftad/user-ip` | Create AD user/IP mapping |
| POST | `/api/v3/microsoftad/triggerSync` | Trigger AD sync |
| GET | `/api/v3/microsoftad/getADQueryStatus` | Get AD query status |

#### Secure Access Application (SAA)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/access/application` | Get all remote access applications |
| POST | `/api/v3/access/application` | Create remote access application |
| PUT | `/api/v3/access/application/{id}` | Update application |
| DELETE | `/api/v3/access/application/{id}` | Delete application |
| GET | `/api/v3/access/application/get/{site_id}` | Get applications by site |
| GET | `/api/v3/access/application/types` | Get application types |
| GET | `/api/v3/access/application/approvals` | Get pending approvals |
| POST | `/api/v3/access/application/request-approval/{application_id}` | Request approval |
| GET | `/api/v3/access/application/lastUpdatedTime` | Last updated time |
| GET | `/api/v3/access/application/profiles` | Get access profiles |
| POST | `/api/v3/access/application/profile` | Create access profile |
| PUT | `/api/v3/access/application/profile/{id}` | Update access profile |
| DELETE | `/api/v3/access/application/profile/{id}` | Delete access profile |
| GET | `/api/v3/access/config` | Get SAA config |
| POST | `/api/v3/access/config` | Update SAA config |
| GET | `/api/v3/access/user` | Get remote access users |
| POST | `/api/v3/access/user` | Create remote access user |
| PUT | `/api/v3/access/user/{id}` | Update user |
| DELETE | `/api/v3/access/user/{id}` | Delete user |
| GET | `/api/v3/access/user/code/{id}` | Get activation code |
| POST | `/api/v3/access/user/code/{id}` | Generate new activation code |
| GET | `/api/v3/access/user/lastUpdatedTime` | Users last updated time |
| POST | `/api/v3/access/user/okta-sync` | Sync Okta users |
| GET | `/api/v3/access/group-policies` | Get group policies |
| POST | `/api/v3/access/group-policies` | Create group policy |
| DELETE | `/api/v3/access/group-policies` | Delete all group policies |
| GET | `/api/v3/access/group-policies/{policy_id}` | Get policy by ID |
| PUT | `/api/v3/access/group-policies/{policy_id}` | Update policy |
| DELETE | `/api/v3/access/group-policies/{policy_id}` | Delete policy |
| GET | `/api/v3/access/group-policies/name/{policy_name}` | Get policy by name |
| PUT | `/api/v3/access/group-policies/name/{policy_name}` | Update policy by name |
| DELETE | `/api/v3/access/group-policies/name/{policy_name}` | Delete policy by name |
| POST | `/api/v3/access/group-policies/bulk` | Bulk create policies |
| PUT | `/api/v3/access/group-policies/bulk` | Bulk update policies |
| GET | `/api/v3/access/group-policies/approval-rules` | Get approval rules |
| GET | `/api/v3/access/group-policies/approve/{id}/{period}` | Approve SAA access |
| GET | `/api/v3/access/group-policies/check-access` | Check user access |
| GET | `/api/v3/access/group-policy-rules` | Get all policy rules |
| POST | `/api/v3/access/group-policy-rules` | Create policy rule |
| DELETE | `/api/v3/access/group-policy-rules` | Delete all rules |
| GET | `/api/v3/access/group-policy-rules/{rule_id}` | Get rule by ID |
| PUT | `/api/v3/access/group-policy-rules/{rule_id}` | Update rule |
| DELETE | `/api/v3/access/group-policy-rules/{rule_id}` | Delete rule |
| GET | `/api/v3/access/group-policy-rules/last-update-time` | Last update time |
| GET | `/api/v3/access/group-membership` | Get group membership |
| GET | `/api/v3/access/group-membership/groups` | Get groups by IP prefix |
| GET | `/api/v3/access/group-membership/last-update-time` | Membership last update time |
| GET | `/api/v3/access/settings/lastUpdatedTime` | Settings last updated time |
| GET | `/api/v3/access/importexport/template/{templateType}` | Download import template |
| POST | `/api/v3/access/importexport/upload/applications` | Upload applications |
| POST | `/api/v3/access/importexport/upload/users` | Upload users |
| POST | `/api/v3/access/importexport/upload/auth0/users` | Upload Auth0 users |
| POST | `/api/v3/access/importexport/upload/staticroutes` | Upload static routes |
| POST | `/api/v3/access/importexport/upload/app-seg/static-ips` | Upload app segment static IPs |
| POST | `/api/v3/access/importexport/validate/applications` | Validate applications import |
| POST | `/api/v3/access/importexport/validate/users` | Validate users import |
| POST | `/api/v3/access/importexport/validate/auth0/users` | Validate Auth0 users import |
| POST | `/api/v3/access/importexport/validate/staticroutes` | Validate static routes import |
| POST | `/api/v3/access/importexport/validate/app-segment/static-ips` | Validate app segment static IPs |

#### API Key Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v3/api-key-auth/create` | Create API key |
| GET | `/api/v3/api-key-auth/list` | List all API keys |
| POST | `/api/v3/api-key-auth/login` | Login using API key |
| PUT | `/api/v3/api-key-auth/revoke/{id}` | Revoke API key |

#### Templates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/templates` | Get gateway templates |
| POST | `/api/v3/templates` | Create gateway template |
| GET | `/api/v3/templates/{id}` | Get template by ID |
| PUT | `/api/v3/templates/{id}` | Update template |
| DELETE | `/api/v3/templates/{id}` | Delete template |
| GET | `/api/v3/templates/names` | Get template names |
| GET | `/api/v3/templates/interfaces/{platform}` | Get template interfaces by platform |
| POST | `/api/v3/templates/{id}/clone` | Clone template |
| POST | `/api/v3/templates/{id}/deploy_site` | Deploy site from template |
| GET | `/api/v3/templates/{id}/interfaces` | Get template interfaces |
| POST | `/api/v3/templates/{id}/interface` | Create template interface |
| PUT | `/api/v3/templates/{id}/interface/{interface_id}` | Update template interface |
| DELETE | `/api/v3/templates/{id}/interface/{interface_id}` | Delete template interface |
| GET | `/api/v3/templates/{id}/vlans` | Get template VLANs |
| POST | `/api/v3/templates/{id}/vlan` | Create template VLAN |
| PUT | `/api/v3/templates/{id}/vlan/{vlan_id}` | Update template VLAN |
| DELETE | `/api/v3/templates/{id}/vlan/{vlan_id}` | Delete template VLAN |
| GET | `/api/v3/templates/{id}/policies` | Get template policies |
| POST | `/api/v3/templates/{id}/policies` | Bulk create template policies |
| PUT | `/api/v3/templates/{id}/policies` | Bulk update template policies |
| DELETE | `/api/v3/templates/{id}/policies` | Bulk delete template policies |
| POST | `/api/v3/templates/{id}/policies/resequence` | Resequence template policies |
| GET | `/api/v3/templates/pbr/policies` | Get template PBR policies |
| POST | `/api/v3/templates/pbr/policies` | Create template PBR policy |
| PUT | `/api/v3/templates/pbr/policies` | Update template PBR policy |
| DELETE | `/api/v3/templates/pbr/policies` | Delete template PBR policy |
| POST | `/api/v3/templates/pbr/policies-reorder` | Reorder template PBR policies |

#### SSL Certificates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/sslcertificates` | Get all SSL certificates |
| POST | `/api/v3/sslcertificates` | Create SSL certificate |
| PUT | `/api/v3/sslcertificates/{id}` | Update SSL certificate |
| GET | `/api/v3/sslcertificates/{siteID}` | Get certificates by site |
| GET | `/api/v3/sslcertificates/lastUpdatedTime` | Last updated time |
| GET | `/api/v3/sslcertificates/lastUpdatedTimeBySiteID/{siteID}` | Last updated time by site |

#### Settings (v3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/settings` | Get all settings |
| PUT | `/api/v3/settings` | Update settings |
| GET | `/api/v3/settings/gwimages` | Get gateway image files by version |
| POST | `/api/v3/settings/gwimages/{version}/files` | Get image files for version |
| GET | `/api/v3/settings/locations` | Get all locations |
| GET | `/api/v3/settings/mqtt-broker-url` | Get MQTT broker URL |
| GET | `/api/v3/settings/snmp-config` | Get SNMP config |
| PUT | `/api/v3/settings/snmp-config` | Update SNMP config |
| GET | `/api/v3/settings/sso-config` | Get SSO settings |
| PUT | `/api/v3/settings/sso-config` | Update SSO settings |
| PUT | `/api/v3/settings/reset-kibana-credentials` | Reset Kibana credentials |
| GET | `/api/v3/settings/download-snmp-mib` | Download SNMP MIB |
| GET | `/api/v3/settings/ra-dns-servers` | Get RA DNS server config |
| POST | `/api/v3/settings/ra-dns-servers` | Add RA DNS server config |
| GET | `/api/v3/settings/ra-dns-lastupdated` | RA DNS last updated time |
| PUT | `/api/v3/settings/app-segment/static-ips-mapping` | Update app segment static IPs mapping |
| GET | `/api/v3/settings/app-segment/static-ips/global` | Get app segment static IPs mapping |
| GET | `/api/v3/settings/app-segment/static-ips/export` | Export static IPs mapping |
| GET | `/api/v3/settings/app-segment/static-ips/last-update-time` | Static IPs last update time |

#### NSG Channels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/settings/nsg/channels` | List NSG channels |
| POST | `/api/v3/settings/nsg/channels` | Create channel |
| GET | `/api/v3/settings/nsg/channels/prototypes` | Channel prototypes |
| GET | `/api/v3/settings/nsg/channels/{channel_id}` | Get channel by ID |
| PUT | `/api/v3/settings/nsg/channels/{channel_id}` | Update channel |
| DELETE | `/api/v3/settings/nsg/channels/{channel_id}` | Delete channel |
| PATCH | `/api/v3/settings/nsg/channels/{channel_id}/devices` | Bulk add channel to devices |
| GET | `/api/v3/settings/nsg/secrets/{secret_path}` | Get secret |

#### Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/payments/plans` | Get offered plans |
| POST | `/api/v3/payments/subscription` | Initiate subscription |
| DELETE | `/api/v3/payments/subscription` | Delete subscription |
| POST | `/api/v3/payments/activateSubscription` | Activate subscription |
| GET | `/api/v3/payments/userplans` | Get user plans |
| POST | `/api/v3/payments/userplans` | Add user plan |

#### Policy Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/policy-comments/comment/{policyId}` | Get comments for policy |
| POST | `/api/v3/policy-comments/comment/{policyId}` | Add comment |
| PUT | `/api/v3/policy-comments/comment/{commentId}` | Update comment |
| DELETE | `/api/v3/policy-comments/comment/{commentId}` | Delete comment |

#### Debug Manager

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/debug-manager/resource-status` | Get gateway resource stats |
| POST | `/api/v3/debug-manager/resource-status` | Update gateway resource stats |

#### ZTNA Client

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/ztnaclient/releases` | Get client release versions |
| GET | `/api/v3/ztnaclient/checkupdate` | Check for update |
| GET | `/api/v3/ztnaclient/getimageurl/{os_type}` | Get client download URL |
| GET | `/api/v3/ztnaclient/getlogurl` | Get log upload URL |
| POST | `/api/v3/ztnaclient/register/{os_type}/{uuid}` | Register client |
| POST | `/api/v3/ztnaclient/tunnellife` | Set tunnel life |
| POST | `/api/v3/ztnaclient/upgrade` | Upgrade client |
| POST | `/api/v3/ztnaclient/upgradestatus` | Upgrade status |

#### Customer Logo (v3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/customer/ui/logo` | Get customer logo |

---

## Common Patterns

### Create site + network + gateway
```
1. POST /api/v2/Site/           → create site
2. POST /api/v2/Network/        → create network (VLAN) on site
3. POST /api/v2/Gateway/        → create gateway in site
4. POST /api/v2/Gateway/sendactivationlink → send activation to gateway
```

### Configure IPsec tunnel to ZIA
```
1. GET  /api/v2/cluster/ipsec-config    → check existing config
2. POST /api/v2/cluster/ipsec-config    → configure IPsec with ZIA DC IP
3. GET  /api/v2/cluster/ipsec-status    → verify tunnel UP
```

### Add PBR rule for traffic steering
```
1. GET  /api/v3/pbr/interfaces?gateway_id=<id>  → discover interfaces
2. GET  /api/v3/pbr/policies?gateway_id=<id>    → list existing policies
3. POST /api/v3/pbr/policies                     → create new PBR policy
4. POST /api/v3/pbr/policies-reorder             → reorder as needed
```

### Configure VRRP for HA
```
1. GET  /api/v3/vrrp/config/{cluster_id}    → current VRRP config
2. POST /api/v3/vrrp/config/{cluster_id}    → update VRRP config
3. GET  /api/v3/vrrp/vrrpstatus/{cluster_id} → verify HA status
```

### Deploy from template
```
1. GET  /api/v3/templates                          → list templates
2. POST /api/v3/templates/{id}/deploy_site         → deploy site from template
```

### Configure dynamic routing
```
1. POST /api/v3/Bgp/config      → add BGP peer
2. GET  /api/v3/Bgp/bgpstatus/{cluster_id} → verify BGP session
# Or for OSPF:
1. POST /api/v3/Ospf/config     → add OSPF config
```

---

## Known Limitations

1. **No MCP tools** -- all operations require direct HTTP calls to the AirGap API
2. **AirGap API is separate from OneAPI** -- different base URL (`*.goairgap.com`), same OAuth2 token
3. **`dns_servers` field is read-only via API** -- PUT returns 200 OK but does not change the value
4. **Transparent DNS proxy** intercepts ALL port 53 at L7 before PBR rules apply; to bypass, move traffic outside ZTB VLANs or use DoH
5. **PBR endpoints require `?gateway_id=`** query parameter -- calls without it will fail
6. **v2 vs v3 migration** -- some endpoints moved from v2 to v3 (PBR, VRRP, devices, BGP, OSPF); if one version returns 404, try the other
7. **Cloud Connector API** is a separate API at `connector.<cloud>.net/api/v1` -- not covered here
