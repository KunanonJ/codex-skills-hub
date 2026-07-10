---
name: aside-aside
description: >-
  Use this when you need to inspect or update Aside daemon settings, sessions, routine, task transcripts, child sessions, or session runtime config.
metadata:
  version: "0.1.0"
---
# Aside

Use the `aside` global in the REPL tool to inspect account settings and session/task state.
Prefer reads first. Only call write methods when the user asks for a settings/session change or the task clearly requires it.

## Quick Reference

```js
const allSettings = aside.settings.getAll();
const memory = aside.settings.get('memory');
aside.settings.set('memory', { ...memory, enabled: true });

const recent = aside.sessions.list({ limit: 10 });
const current = aside.sessions.current();
const session = aside.sessions.get('session-id');
const messages = aside.sessions.messages('session-id', { limit: 40, order: 'asc' });
const rows = aside.sessions.messageRows('session-id');
const children = aside.sessions.childSessions('session-id');

const routines = aside.routines.list({ limit: 10 });
const routine = aside.routines.get('routine-id');
```

## Settings

### `aside.settings.getAll(): SettingsData`

Returns account-scoped daemon settings from `settings.json`.

### `aside.settings.get(key): SettingsData[key]`

Read one setting key such as `defaultModel`, `modelCategories`, `followUpBehavior`, `selectionOverlay`, `memory`, `compaction`, or `retry`.

### `aside.settings.set(key, value): SettingsData`

Replace one setting key after schema validation.
Always read the existing value first and preserve unrelated fields.

```js
const current = aside.settings.get('compaction');
aside.settings.set('compaction', { ...current, enabled: false });
```

## Sessions

Session methods return concise metadata and omit bulky fields like `systemPrompt`, `toolState`, and queued message bodies.

### `aside.sessions.current(): SessionSummary | undefined`

Returns the current agent session when the REPL is running inside one.

### `aside.sessions.list(options?): SessionSummary[]`

List sessions. Defaults to visible, non-archived, root sessions, newest first, limit 20.

Useful options:
```ts
{
  agentId?: string;
  order?: 'desc' | 'asc';
  cursor?: number;
  limit?: number; // max 200
}
```

### `aside.sessions.get(sessionId?): SessionSummary`

Get one session. `sessionId` is optional only inside a real agent session.

### `aside.sessions.messages(sessionId?, options?): AgentMessage[]`

Read transcript messages. Default: first 50 messages in ascending order. Use a small limit before printing.

```js
const messages = aside.sessions.messages('session-id', { limit: 20, order: 'asc' });
console.log(messages.map(m => ({ role: m.role, content: m.content })).slice(-5));
```

### `aside.sessions.messageRows(sessionId?): { id, role, timestamp }[]`

Read ordered message row IDs for exact transcript cutoffs or branch points.

### `aside.sessions.childSessions(parentId?, options?): SessionSummary[]`

List child/subagent sessions. Pass `{ triggeredBy }` to scope to one triggering tool call.

### `aside.sessions.update(sessionId, patch): SessionSummary`

Update safe session metadata/config only: `title`, `activeTabTargetId`, `model`, `permissionMode`, `permission`, and `runtimeConfig`.
Changing `permissionMode` also rewrites the concrete permission config used by runtime hooks.

```js
aside.sessions.update('session-id', {
  runtimeConfig: { proactiveMode: true },
});
```

### `aside.sessions.archive(sessionId)` / `unarchive(sessionId)`

Archive or restore a session. Do this only when the user asks.

### `aside.sessions.markRead(sessionId)` / `markUnread(sessionId)`

Update task unread state.

## Routines

Routine methods return saved routine definitions, including schedule, prompt, status cursor, and target session metadata.
For update and delete, use `routine_update` tool. This skill provides read-only APIs. 

### `aside.routines.list(options?): Routine[]`

List non-deleted routines. Defaults to newest updated first, limit 20.

Useful options:
```ts
{
  agentId?: string;
  limit?: number; // max 200
}
```

### `aside.routines.get(id): Routine`

Get one routine by id, including paused or deleted routines.
