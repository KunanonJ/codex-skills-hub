---
name: cursor-plugin-postman-agent-ready-apis
description: >-
  Knowledge about AI agent API compatibility. Use when user asks about API readiness, agent compatibility, or wants to improve their API for AI consumption.
metadata:
  version: "0.1.0"
---

# Agent-Ready APIs

Knowledge about what makes an API "agent-ready" for AI agent consumption.

## What Agent-Readiness Means

An agent-ready API is one that an AI agent can:
1. **Discover** -- Find the right endpoint for a given task
2. **Understand** -- Construct a valid request without guessing
3. **Self-heal** -- Recover from errors without human intervention

Most APIs are built for human developers who can read docs, interpret ambiguous errors, and make judgment calls. AI agents can't do that. They need explicit metadata, structured errors, and predictable patterns.

## The 8 Pillars

Agent-readiness is measured across 8 pillars with 48 total checks. See `pillars.md` for the complete reference.

| Pillar | What It Measures |
|--------|-----------------|
| **Metadata** | operationIds, summaries, descriptions, tags |
| **Errors** | Error schemas, HTTP codes, messages, retry guidance |
| **Introspection** | Parameter types, required fields, enums, examples |
| **Naming** | Consistent casing, RESTful paths, HTTP method semantics |
| **Predictability** | Response schemas, pagination patterns, date formats |
| **Documentation** | Auth docs, rate limits, external references |
| **Performance** | Response times, caching headers, rate limit headers |
| **Discoverability** | OpenAPI version, server URLs, contact info, license |

## Scoring

- Each check has a severity: Critical (4x weight), High (2x), Medium (1x), Low (0.5x)
- Score is 0-100 based on weighted pass/fail
- **Agent Ready** = score >= 70% with zero critical failures
- A single critical failure (like missing operationIds) means "not agent-ready" regardless of total score

## When to Suggest Analysis

Suggest running the readiness analyzer when:
- User says "is my API agent-ready?" or "ready for AI agents?"
- User asks "what's wrong with my API?"
- User mentions building an AI agent that consumes their API
- User asks about MCP server compatibility
- User wants to improve their API for LLM tool use
- User mentions they're building tools for Claude, GPT, Gemini, or other AI models

## How to Interpret Scores

| Score | Verdict | What It Means |
|-------|---------|---------------|
| 90-100 | Excellent | API is highly agent-compatible. Minor improvements only. |
| 70-89 | Agent Ready | Meets the bar. Some improvements recommended. |
| 50-69 | Needs Work | Agents will struggle. Address critical and high issues. |
| 0-49 | Not Ready | Significant gaps. Agents will fail frequently. |

## Common Quick Wins

These fixes have the highest impact-to-effort ratio:

1. **Add operationIds to every endpoint** (+8-15 points). Agents use these to select endpoints.
2. **Define error response schemas** (+5-10 points). Agents need to parse and recover from errors.
3. **Add parameter examples** (+3-5 points). Agents use examples as templates for valid requests.
4. **Document rate limits** (+3-5 points). Agents need to know their constraints.
5. **Use consistent naming** (+2-4 points). Agents predict URL patterns from names.
