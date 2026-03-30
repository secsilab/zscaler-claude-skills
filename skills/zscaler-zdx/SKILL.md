---
name: zscaler-zdx
description: Use when working with ZDX (Digital Experience) — application monitoring, device metrics, alerts, user experience scores, deep traces, software inventory.
---

# Zscaler Digital Experience (ZDX)

## Overview
ZDX monitors end-user digital experience. Use for application performance, device health, alerts, deep traces, and software inventory.

## MCP Tools
Available MCP tools: `zdx_list_applications`, `zdx_get_application`, `zdx_list_devices`, `zdx_get_device`, `zdx_list_alerts`, `zdx_get_alert`, `zdx_list_application_users`, `zdx_get_application_user`, `zdx_get_application_score_trend`, `zdx_get_application_metric`, `zdx_list_departments`, `zdx_list_locations`, `zdx_list_software`, `zdx_get_software_details`, `zdx_list_device_deep_traces`, `zdx_get_device_deep_trace`, `zdx_list_historical_alerts`.

## API Reference

### administration (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/administration/departments` | /administration/departments |
| GET | `/administration/locations` | /administration/locations |
| GET | `/active_geo` | /active_geo |

### reports (20 endpoints)

#### apps

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/apps/{{appID}}/users` | apps/{{appID}}/users |
| GET | `/apps/{{appID}}/users/{{userID}}` | apps/{{appID}}/users/{userid} |
| GET | `/apps/{{appID}}` | apps/{appID} |
| GET | `/apps/{{appID}}/score` | apps/{appID}/score |
| GET | `/apps/{{appID}}/metrics` | apps/{appID}/metrics |
| GET | `/apps` | /apps |

#### devices

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/devices/{{deviceID}}/apps/{{deviceAppID}}/cloudpath-probes` | /devices/{deviceID}/apps/{appid}/cloudpath-probes |
| GET | `/devices/{{deviceID}}/apps/{{deviceAppID}}/cloudpath-probes/{{cloudProbeId}}` | /devices/{deviceID}/apps/{appid}/cloudpath-probes/{probeid} |
| GET | `/devices/{{deviceID}}/apps/{{deviceAppID}}/cloudpath-probes/{{cloudProbeId}}/cloudpath` | /devices/{deviceID}/apps/{appid}/cloudpath-probes/{probeid}/cloudpath Copy |
| GET | `/devices/{{deviceID}}/apps/{{deviceAppID}}/web-probes` | /devices/{deviceID}/apps/{appid}/web-probes |
| GET | `/devices/{{deviceID}}/apps/{{deviceAppID}}/web-probes/{{webProbeId}}` | /devices/{deviceID}/apps/{appid}/web-probes/{probeid} |
| GET | `/devices/{{deviceID}}/apps/{{deviceAppID}}` | /devices/{deviceID}/apps/{deviceAppID}/ |
| GET | `/devices/{{deviceID}}/apps/{{deviceAppID}}/call-quality-metrics` | /devices/{deviceID}/apps/{deviceAppID}/call-quality-metrics |
| GET | `/devices/{{deviceID}}/apps` | /devices/{deviceID}/apps |
| GET | `/devices/{{deviceID}}` | devices/{deviceID} |
| GET | `/devices/{{deviceID}}/health-metrics` | devices/{deviceID}/health-metrics |
| GET | `/devices/{{deviceID}}/events` | devices/{deviceID}/events |
| GET | `/devices` | /devices |

#### users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | /users |
| GET | `/users/{{userID}}` | /users/{{userID}} |

### troubleshooting (12 endpoints)

#### deeptraces

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/devices/{{deviceID}}/deeptraces/{{trace_id}}` | /devices/{{deviceID}}/deeptraces/{{trace_id}} |
| DELETE | `/devices/{{deviceID}}/deeptraces/{{trace_id}}` | /devices/{{deviceID}}/deeptraces/{{trace_id}} |
| GET | `/devices/{{deviceID}}/deeptraces/{{trace_id}}/webprobe-metrics` | /devices/{{deviceID}}/deeptraces/{{trace_id}}/webprobe-metrics |
| GET | `/devices/{{deviceID}}/deeptraces/{{trace_id}}/cloudpath-metrics` | /devices/{{deviceID}}/deeptraces/{{trace_id}}/cloudpath-metrics |
| GET | `/devices/{{deviceID}}/deeptraces/{{trace_id}}/cloudpath` | /devices/{{deviceID}}/deeptraces/{{trace_id}}/cloudpath |
| GET | `/devices/{{deviceID}}/deeptraces/{{trace_id}}/health-metrics` | /devices/{{deviceID}}/deeptraces/{{trace_id}}/health-metrics |
| GET | `/devices/{{deviceID}}/deeptraces/{{trace_id}}/top-processes` | /devices/{{deviceID}}/deeptraces/{{trace_id}}/top-processes |
| GET | `/devices/{{deviceID}}/deeptraces` | /devices/{{deviceID}}/deeptraces |
| POST | `/devices/{{deviceID}}/deeptraces` | /devices/{{deviceID}}/deeptraces |

#### analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analysis/{{analysisID}}` | /analysis/{analysisID} |
| DELETE | `/analysis/{{analysisID}}` | /analysis/{analysisID} |
| POST | `/analysis` | /analysis |

### alerts (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/alerts/ongoing` | /alerts/ongoing |
| GET | `/alerts/historical` | /alerts/historical |
| GET | `/alerts/{{alertID}}` | /alerts/{{alertID}} |
| GET | `/alerts/{{alertID}}/affected_devices` | /alerts/{{alertID}}/affected_devices |

### Software Inventory (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/software` | /inventory/software |
| GET | `/inventory/software/{{software_key}}` | /inventory/software/{software_key} |

### Snapshots (1 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/snapshot/alert` | Share a Snapshot |

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zdx/api/v1`

## Common Patterns
- Check application health score trends
- List alerts for a specific timeframe
- Get device deep trace for troubleshooting
- List software inventory across fleet

## Known Limitations
- All MCP tools are read-only
- Alert acknowledgment requires direct API
