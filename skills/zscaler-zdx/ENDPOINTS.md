<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->
# Zscaler Digital Experience (ZDX) API Reference

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

