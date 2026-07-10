---
name: cursor-plugin-postman-rule-postman-best-practices
description: >-
  API design best practices for Postman-managed APIs. Applied when working with OpenAPI specs, collections, and API code.
metadata:
  version: "0.1.0"
---

# Postman API Best Practices

Follow these conventions when creating, modifying, or reviewing APIs and OpenAPI specs.

## Naming Conventions

- Use **kebab-case** for URL paths: `/user-profiles`, not `/userProfiles` or `/user_profiles`
- Use **plural nouns** for collection resources: `/users`, `/orders`, `/products`
- Use **singular nouns** for singleton resources: `/users/{id}/profile`
- Avoid verbs in paths. Use HTTP methods to convey action:
  - `POST /users` (not `/createUser`)
  - `DELETE /orders/{id}` (not `/deleteOrder`)
- Use **camelCase** for JSON properties: `firstName`, `createdAt`, `userId`
- Use consistent property naming across all endpoints

## HTTP Method Semantics

| Method | Purpose | Idempotent | Success Code |
|--------|---------|------------|--------------|
| GET | Read resource(s) | Yes | 200 |
| POST | Create resource | No | 201 |
| PUT | Replace resource | Yes | 200 |
| PATCH | Partial update | No | 200 |
| DELETE | Remove resource | Yes | 204 |

## OpenAPI Spec Standards

Every endpoint MUST have:
- `operationId`: Unique, camelCase identifier (e.g., `getUser`, `createOrder`)
- `summary`: Short description under 120 characters
- `tags`: At least one tag for grouping
- `responses`: At minimum, define the success response and common errors (400, 401, 404, 500)

Every parameter MUST have:
- `type` or `schema` with explicit type
- `description`: What the parameter does
- `required`: Explicitly set to true or false
- `example`: A realistic example value

## Error Response Standard

All error responses should follow a consistent schema:

```yaml
components:
  schemas:
    Error:
      type: object
      required: [error, code]
      properties:
        error:
          type: string
          description: Human-readable error message
        code:
          type: string
          description: Machine-readable error code
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
```

Define these error responses on every endpoint:
- `400`: Validation error (with field-level details)
- `401`: Authentication required
- `403`: Insufficient permissions
- `404`: Resource not found (on endpoints with path parameters)
- `429`: Rate limit exceeded (with Retry-After header)
- `500`: Internal server error

## Pagination

List endpoints returning multiple items MUST support pagination:

```yaml
parameters:
  - name: limit
    in: query
    schema:
      type: integer
      default: 20
      maximum: 100
  - name: offset
    in: query
    schema:
      type: integer
      default: 0
```

Response should include pagination metadata:
```yaml
properties:
  data:
    type: array
    items: ...
  meta:
    type: object
    properties:
      total:
        type: integer
      limit:
        type: integer
      offset:
        type: integer
```

## Authentication

- Document security schemes in the `components.securitySchemes` section
- Apply security globally or per-endpoint (never leave endpoints unprotected by accident)
- Use Bearer tokens or API keys in headers (not query parameters)
- Mark auth-related environment variables as `secret` type in Postman

## Collection Organization

When creating Postman collections:
- Group endpoints by resource in folders (Users, Orders, Products)
- Include at least one example response per request
- Set collection-level auth (inherited by all requests)
- Use environment variables for base URL, tokens, and config
- Add pre-request scripts for auth token refresh if needed
- Add test scripts to validate response structure

## Dates and Formats

- Use **ISO 8601** for all dates: `2026-01-15T10:30:00Z`
- Use `format: date-time` in schemas for datetime fields
- Use `format: date` for date-only fields
- Use `format: email` for email fields
- Use `format: uri` for URL fields

## Versioning

- Include version in the API info: `info.version: "1.0.0"`
- Use URL path versioning (`/v1/users`) or header versioning
- Mark deprecated endpoints with `deprecated: true`
- Document migration path in the description of deprecated endpoints
