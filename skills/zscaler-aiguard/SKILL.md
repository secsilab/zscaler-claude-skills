---
name: zscaler-aiguard
version: 1.1.0
postman_revision: 2026-03-30
description: Use when working with Zscaler AI Guard — content detection, policy execution for AI/ML content inspection, n8n integration, NeMo Guardrails, AI Gateway.
---

# Zscaler AI Guard

## Overview
AI Guard inspects content against AI/ML security policies. Use for detecting sensitive data in AI prompts/responses and enforcing content policies.

## MCP Tools
No MCP tools. Direct API calls only.


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication
Bearer token authentication. Base URL: `https://{{ZAIGuardBase}}/detection`

## Common Patterns
- Inspect outbound AI prompt content: `POST /detection/resolve-and-execute-policy` with `direction=OUT`
- Inspect inbound AI response content: `POST /detection/resolve-and-execute-policy` with `direction=IN`
- Execute specific policy by ID: `POST /detection/execute-policy` with `policy_id`

## Known Limitations
- Only 2 endpoints — early-stage product
- No MCP tools
- Policy creation/management not available via API (admin portal only)

## Integration Ecosystem

AI Guard extends beyond its core API through several integration points:

### n8n Community Node (`n8n-nodes-aiguard`)

A community-built n8n node that enables AI Guard inspection within n8n workflow automation. Use this to insert AI Guard content detection into automated pipelines (e.g., inspect LLM outputs before they are written to external systems, or inspect user inputs before forwarding to an LLM).

- **Package:** `n8n-nodes-aiguard` (npm)
- **Use case:** No-code/low-code automation workflows that need AI content policy enforcement
- **Supports:** Both `direction=IN` and `direction=OUT` inspection modes

### NeMo Guardrails (`aiguard-nemo-guardrails`)

An integration package for NVIDIA NeMo Guardrails that uses AI Guard as a content safety rail. NeMo Guardrails is a framework for adding guardrails (topic restrictions, safety filters, fact-checking) to LLM applications.

- **Package:** `aiguard-nemo-guardrails` (Python)
- **Use case:** Enterprise LLM applications built on NeMo that need enterprise-grade content policy (DLP, compliance)
- **Architecture:** Runs as a NeMo rail action; calls AI Guard API for each LLM turn

### AI Gateway

AI Gateway is a Zscaler platform feature that proxies and inspects traffic between users and AI/LLM services (e.g., ChatGPT, Copilot, Claude). AI Guard policy is the enforcement layer within AI Gateway.

- **Relationship:** AI Gateway routes traffic; AI Guard provides content inspection and policy execution
- **Configuration:** AI Guard policies are applied within the AI Gateway configuration in the Zscaler admin portal
- **Coverage:** Supports both browser-based AI access (via ZIA proxy) and API-level AI calls

### Integration Architecture

```
User / App → [AI Gateway (routing + auth)] → [AI Guard (content inspection)]
                                                      ↓
                                             Policy: allow / block / redact / audit
```

When building integrations, prefer the AI Gateway + AI Guard combination for complete visibility. The n8n node and NeMo integration are for custom pipeline insertion where AI Gateway cannot intercept traffic natively.
