---
name: cursor-plugin-postman-postman-routing
description: >-
  Automatically routes Postman and API-related requests to the correct command. Use when user mentions APIs, collections, specs, testing, mocks, docs, security, or Postman.
metadata:
  version: "0.1.0"
---

# Postman Command Router

When a user mentions anything related to APIs, Postman, collections, specs, or API development, automatically route to the correct command. Do not ask the user to pick a command. Just invoke the right one.

## Intent-to-Command Mapping

| User intent patterns | Route to | Command |
|---------------------|----------|---------|
| "sync", "update collection", "create collection", "import spec", "push to postman", "keep in sync", "deploy spec" | Sync collections with code | `/postman:sync` |
| "generate", "client", "code for", "wrapper", "SDK", "consume", "typed client", "api client" | Generate client code | `/postman:codegen` |
| "find", "search", "what endpoints", "is there an API for", "show me", "what's available", "discover", "list APIs" | Discover APIs | `/postman:search` |
| "test", "run tests", "check if", "validate", "test results", "failing tests" | Run collection tests | `/postman:test` |
| "mock", "fake API", "stub", "mock server", "frontend needs", "mock URL" | Create mock server | `/postman:mock` |
| "docs", "documentation", "describe", "document", "API reference", "missing descriptions" | Improve documentation | `/postman:docs` |
| "security", "audit", "OWASP", "vulnerabilities", "secure", "auth check", "exposed" | Security audit | `/postman:security` |
| "agent-ready", "AI compatible", "scan my API", "grade my API", "readiness", "agent friendly" | API readiness analysis | Invoke `readiness-analyzer` agent |
| "set up", "configure", "connect postman", "API key", "get started" | First-run setup | `/postman:setup` |

## Routing Priority

1. **Exact command match** -- If the user types `/postman:sync`, run that command directly
2. **Strong intent match** -- If the user says "generate a TypeScript client for the payments API", that's clearly `/postman:codegen`
3. **Contextual match** -- If the user is working on a spec and says "push this to Postman", that's `/postman:sync`
4. **Ambiguous** -- If intent is unclear, ask: "I can help you sync collections, generate client code, search for APIs, run tests, create mocks, improve docs, or audit security. What do you need?"

## When to Use Commands vs. Raw MCP Tools

- **Use commands** for multi-step workflows (syncing, codegen, testing). Commands handle the full flow including error handling, async polling, and result formatting.
- **Use raw MCP tools** for simple one-off queries ("What workspaces do I have?" -> just call `getWorkspaces`).

## Common Compound Workflows

Some requests span multiple commands:

| Request | Workflow |
|---------|----------|
| "Set up my API from scratch" | `/postman:sync` (create collection) -> `/postman:mock` (create mock) -> `/postman:docs` (generate docs) |
| "Is my API production-ready?" | `/postman:security` (audit) + `/postman:test` (run tests) + readiness-analyzer (if agent-readiness asked) |
| "I updated my spec, sync and re-test" | `/postman:sync` (push changes) -> `/postman:test` (run collection) |
