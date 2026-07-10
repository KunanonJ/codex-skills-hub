---
name: cursor-plugin-postman-postman-knowledge
description: >-
  Postman concepts and MCP tool guidance. Loaded when working with Postman MCP tools to make better decisions about tool selection and workarounds.
metadata:
  version: "0.1.0"
---

# Postman Knowledge Base

Core Postman concepts and MCP tool guidance for making better decisions when working with Postman APIs.

## Core Concepts

- **Collection:** A group of API requests organized in folders. The primary unit of work in Postman. Contains requests, examples (saved responses), test scripts, and documentation. Think of it as a living API reference.

- **Environment:** A set of key-value pairs (variables) scoped to a context like dev, staging, or prod. Used to swap base URLs, auth tokens, and config without changing the requests themselves.

- **Workspace:** A container for collections, environments, specs, mocks, and monitors. Can be personal, team, or public. Most users have one primary workspace.

- **Spec (Spec Hub):** An OpenAPI or AsyncAPI definition stored in Postman. Can generate collections automatically and stay synced with them. The source of truth for API shape.

- **Request:** A single API call definition: HTTP method, URL, headers, body, query params, and test scripts. Lives inside a collection, optionally inside a folder.

- **Response (Example):** A saved example response for a request. Includes status code, headers, and body. Used by mock servers to know what to return and by documentation to show expected responses.

- **Folder:** A grouping within a collection, typically by resource (e.g., "Users", "Orders", "Products"). Can contain requests and nested folders.

- **Tags:** Labels on collections for categorization and search. Useful for finding related APIs.

- **Monitor:** A scheduled collection runner that checks API health. Runs on a cron schedule and alerts on failures.

- **Mock Server:** A fake API that returns example responses from a collection. Used for frontend development before the real API is ready, or for testing in isolation.

## When to Use What

| Goal | Approach |
|------|----------|
| Push code changes to Postman | Spec Hub + sync (`createSpec` -> `syncCollectionWithSpec`) |
| Consume a Postman API in code | Read collection + codegen (`getCollection` -> generate client) |
| Find an API | Search private network (`searchPostmanElementsInPrivateNetwork`) or user's workspace (`getWorkspaces` + `getCollections`) or public network (`searchPostmanElementsInPublicNetwork`) |
| Test an API | Run collection (`runCollection` with environment) |
| Fake an API for frontend | Mock server (`createMock` from collection with examples) |
| Document an API | Analyze collection completeness, fill gaps, improve descriptions |
| Secure an API | Audit spec and collection against OWASP API Top 10 |

## MCP Tool Selection Guide

### Reading Data
- `getWorkspaces` -- List all accessible workspaces
- `getCollections` -- List collections in a workspace
- `getCollection` -- Get full collection detail (always use full model)
- `getCollectionFolder` -- Get folder contents
- `getCollectionRequest` -- Get request details (method, URL, body, params)
- `getCollectionResponse` -- Get saved example responses
- `getEnvironment` / `getEnvironments` -- Get environment variables
- `getSpecDefinition` -- Get the full OpenAPI/AsyncAPI spec
- `getAllSpecs` -- List all specs in a workspace

### Writing Data
- `createCollection` -- Create new collection (cannot nest folders, use decomposed approach)
- `createCollectionFolder` -- Create folder in collection
- `createCollectionRequest` -- Create request in collection or folder
- `createCollectionResponse` -- Save example response
- `createEnvironment` -- Create environment with variables
- `createSpec` -- Upload OpenAPI spec to Spec Hub
- `updateSpecFile` -- Update an existing spec
- `updateCollectionRequest` -- Modify request details
- `createMock` -- Create mock server from collection

### Syncing
- `syncCollectionWithSpec` -- Update collection from spec (async, OpenAPI 3.0 only)
- `syncSpecWithCollection` -- Update spec from collection changes
- `generateCollection` -- Generate collection from spec (async)

### Running
- `runCollection` -- Execute collection tests

### Searching
- `searchPostmanElementsInPrivateNetwork` -- Search private/org APIs (**default**)
- `searchPostmanElementsInPublicNetwork` -- Search public Postman network
- `getTaggedEntities` -- Find by tag

For detailed limitations and workarounds, see the companion file `mcp-limitations.md`.
