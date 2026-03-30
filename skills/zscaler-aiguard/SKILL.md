---
name: zscaler-aiguard
description: Use when working with Zscaler AI Guard — content detection, policy execution for AI/ML content inspection.
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
