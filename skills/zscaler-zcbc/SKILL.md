---
name: zscaler-zcbc
description: Use when working with ZCBC (Cloud & Branch Connector) via OneAPI — partner integrations, policy resources, admin roles, location management, connector groups.
---

# Zscaler Cloud & Branch Connector (ZCBC)

## Overview
ZCBC manages Cloud Connectors and Branch Connectors via OneAPI (complementary to ZTB AirGap API). Use for partner integrations, policy management, admin roles, and connector lifecycle.

## MCP Tools
No dedicated MCP tools. Use OneAPI directly.

## API Reference

### Activation (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/ecAdminActivateStatus/activate` | Activation - Activate |
| GET | `/ecAdminActivateStatus` | Activation - Status |
| PUT | `/ecAdminActivateStatus/forcedActivate` | Activation - Force Activate |

### Admin and Role Management (11 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/adminRoles` | Admin and Role Management - Get All Admin Roles |
| GET | `/adminRoles` | Admin and Role Management - Get Individual Admin Role |
| POST | `/adminRoles` | Admin and Role Management - Create Admin Role |
| PUT | `/adminRoles/{roleId}` | Admin and Role Management - Update Individual Admin Role |
| DELETE | `/adminRoles/{roleId}` | Admin and Role Management - Delete Individual Admin Role |
| GET | `/adminUsers` | Admin and Role Management - Get All Users |
| GET | `/adminUsers/{userId}` | Admin and Role Management - Get Individual User |
| PUT | `/adminUsers/{userId}` | Admin and Role Management - Update Individual User |
| DELETE | `/adminUsers/{userId}` | Admin and Role Management - Delete Individual User |
| POST | `/adminUsers` | Admin and Role Management - Create User |
| POST | `/passwordChange` | Admin and Role Management - Change Password |

### Cloud & Branch Connector Groups (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ecgroup` | Cloud & Branch Connector Groups - Get All Groups and VMs |
| GET | `/ecgroup/lite` | Cloud & Branch Connector Groups - Get All Groups and VMs (Lite) |
| GET | `/ecgroup/{id}` | Cloud & Branch Connector Groups - Get Individual Group and VMs |
| GET | `/ecgroup/{id}/vm/{vmId}` | Cloud & Branch Connector Groups - Get Individual VM |
| DELETE | `/ecgroup/{id}/vm/{vmId}` | Cloud & Branch Connector Groups - Delete Individual VM |
| GET | `/ecInstance/lite` | Cloud & Branch Connector Groups - Get All EC Instances (Lite) |

### Forwarding Gateways (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/gateways` | Forwarding Gateways - Get all Gateways |
| GET | `/gateways/lite` | Forwarding Gateways - Get all Gateways (Lite) |
| POST | `/gateways` | Forwarding Gateways - Create Gateway |
| DELETE | `/gateways/{gatewayId}` | Forwarding Gateways - Delete Gateway |

### Location Management (9 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/location` | Location Management - Get All Locations |
| GET | `/location/{locationId}` | Location Management - Get Individual Location |
| GET | `/location/lite` | Location Management - Get All Locations (Lite) |
| GET | `/locationTemplate` | Location Management - Get All Location Templates |
| GET | `/locationTemplate/lite` | Location Management - Get All Location Templates (Lite) |
| GET | `/locationTemplate/{locTempId}` | Location Management - Get Individual Location Template |
| POST | `/locationTemplate` | Location Management - Create Location Template |
| PUT | `/locationTemplate/{locTempId}` | Location Management - Update Individual Location Template |
| DELETE | `/locationTemplate/{locTempId}` | Location Management - Delete Individual Location Template |

### Partner Integrations (20 endpoints)

#### Public Cloud Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/publicCloudInfo` | Get All AWS Accounts |
| GET | `/publicCloudInfo/cloudFormationTemplate` | Retrieves the CloudFormation template URL |
| GET | `/publicCloudInfo/count` | Retrieves the total number of AWS accounts |
| GET | `/publicCloudInfo/lite` | Retrieves basic information about the AWS cloud accounts |
| GET | `/publicCloudInfo/supportedRegions` | Retrieves a list of AWS regions |
| GET | `/publicCloudInfo/{{id}}` | Retrieves AWS account details based By ID |
| PUT | `/publicCloudInfo/{{id}}` | Update AWS account details based By ID |
| PUT | `/publicCloudInfo/{{id}}/changeState` | Enables or disables a specific AWS account By ID |
| DELETE | `/publicCloudInfo/{{id}}` | Delete AWS account details based By ID Copy |
| POST | `/publicCloudInfo` | Add New AWS Account |
| POST | `/publicCloudInfo/generateExternalId` | Creates an external ID for an AWS account |

#### Discovery Service

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/discoveryService/workloadDiscoverySettings` | Retrieves the workload discovery service settings |
| PUT | `/discoveryService/{{id}}/permissions` | Verifies the specified AWS account permissions |

#### Account Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accountGroups` | Retrieves the details of AWS account groups |
| GET | `/accountGroups/count` | Retrieves the total number of AWS account groups |
| GET | `/accountGroups/lite` | Retrieves the ID and name of all the AWS account groups |
| GET | `/accountGroups/{{id}}` | Retrieves the specific AWS account group details based on the provided group ID. |
| PUT | `/accountGroups/{{id}}` | Updates the existing AWS account group details based on the provided ID. |
| DELETE | `/accountGroups/{{id}}` | Delete a specific AWS account group |
| POST | `/accountGroups` | Creates an AWS account group |

### Policy Management (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ecRules/ecRdr` | Policy Management - Get All Traffic Forwarding Rules |
| GET | `/ecRules/ecRdr/count` | Policy Management - Get All Traffic Forwarding Rules Count |
| POST | `/ecRules/ecRdr` | Policy Management - Create Traffic Forwarding Rule |
| PUT | `/ecRules/ecRdr/{ruleId}` | Policy Management - Update Traffic Forwarding Rule |

### Provisioning (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/publicCloudAccountDetails` | Provisioning - Get Public Cloud Account Details |
| GET | `/publicCloudAccountDetails/lite` | Provisioning - Get Public Cloud Account Details (Lite) |
| GET | `/publicCloudAccountDetails/{publicCloudAccountId}` | Provisioning - Get Individual Public Cloud Account Details |
| GET | `/publicCloudAccountIdStatus` | Provisioning - Get Public Cloud Account Import Status |
| PUT | `/publicCloudAccountIdStatus` | Provisioning - Enable or Disable Public Cloud Account Import |
| GET | `/provUrl/{provId}` | Provisioning - Get Individual Provisioning Template |
| GET | `/provUrl` | Provisioning - Get All Provisioning Templates |

### Policy Resources (18 endpoints)

#### Network Services

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/networkServices` | Filtering - Get All Network Services |
| POST | `/networkServices` | Filtering - Create Network Service |
| PUT | `/networkServices/{networkServiceId}` | Filtering - Update Network Service |
| DELETE | `/networkServices/{networkServiceId}` | Filtering - Delete Network Service |
| GET | `/networkServiceGroups` | Filtering - Get All Network Service Groups |

#### Source IP Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ipSourceGroups` | Filtering - Get All Source IP Groups |
| GET | `/ipSourceGroups/lite` | Filtering - Get All Source IP Groups (Lite) |
| POST | `/ipSourceGroups` | Filtering - Create Source IP Group |
| DELETE | `/ipSourceGroups/{ipSourceGroupId}` | Filtering - Delete Source IP Group |

#### Destination IP Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ipDestinationGroups` | Filtering - Get All Destination IP Groups |
| GET | `/ipDestinationGroups/lite` | Filtering - Get All Destination IP Groups (Lite) |
| POST | `/ipDestinationGroups` | Filtering - Create Destination IP Group |
| DELETE | `/ipDestinationGroups/{ipGroupId}` | Filtering - Delete Destination IP Group |

#### IP Pools/Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ipGroups` | Filtering - Get All IP Pools/Groups |
| GET | `/ipGroups/lite` | Filtering - Get All IP Pools/Groups (Lite) |
| POST | `/ipGroups` | Filtering - Create IP Pool/Group |
| DELETE | `/ipGroups/{ipGroupId}` | Filtering - Delete IP Pool/Group |

#### ZPA Application Segments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/zpaResources/applicationSegments` | Policy Management - Get All ZPA Application Segments |

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zcbc/api/v1`

## Common Patterns
- List connector groups and their status
- Manage partner integrations
- Configure admin roles for branch management

## Known Limitations
- No MCP tools — all operations via OneAPI direct calls
- For AirGap-level gateway management, use @zscaler-ztb skill instead
