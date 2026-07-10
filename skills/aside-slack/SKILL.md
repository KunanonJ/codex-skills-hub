---
name: aside-slack
description: >-
  Read this when you need to use Slack.
metadata:
  version: "0.1.0"
---
# Slack

Use the `slack` global in the REPL tool. It extracts credentials from the logged-in Slack browser session and returns a `@slack/web-api` WebClient.
No `openTab` is needed- just use the official Slack API.

## IMPORTANT: You should match the tone and writing style same with user's.

Always gather 3-5 user's message writing examples to the channel/person and try to match the tones and writing styles. (and remember it to memory).

The main goal is try to look like the user you're delegating. Be natural like human, and copy habits (e.g., spliting into multiple messages)

## Quick Reference

```js
// List workspaces
const workspaces = await slack.listWorkspaces();
console.log(workspaces);
// → [{ teamId, name, slug, status, memberCount, iconUrl, userId, url, isLastActive? }, ...]

// Get a WebClient for a workspace. IMPORTANT: Save it in a const so you can reuse it in later REPL calls.
const client = await slack.getClient('T05DP5U7M8X');

// List channels
const { channels } = await client.conversations.list({ types: 'public_channel,private_channel', limit: 50 });
console.log(channels.map(c => `#${c.name} (${c.id})`));

// Read messages
const { messages } = await client.conversations.history({ channel: 'C0ARUCEK04A', limit: 20 });
console.log(JSON.stringify(messages, null, 2));

// Post a message
await client.chat.postMessage({ channel: 'C0ARUCEK04A', text: 'Hello from Aside!' });

// Search
const results = await client.search.messages({ query: 'from:alice quarterly report' });
console.log(JSON.stringify(results.messages.matches, null, 2));

// send message with uploading files
await client.filesUploadV2({
  channel_id: 'C0ARUCEK04A',
  thread_ts: '1223313423434.131321', // optional: upload into a thread
  initial_comment: 'Hey <@U05DP5U7M8X>, here are the files you\'ve requested:',
  file_uploads: [
    { file: './logo.png', filename: 'logo.png' },
    { file: './logo-sm.png', filename: 'logo-sm.png' },
  ],
});
// Each entry in `file_uploads` accepts: `file`, `content`, `filename`, `filetype`, `title`, `snippet_type` (e.g. `python`), `alt_text`.
```

## Methods

### `slack.listWorkspaces(): Promise<Workspace[]>`

Fetch all workspaces the user belongs to. Only requires the session cookie — no page tab opened.

Return type:
```ts
interface Workspace {
  teamId: string;       // e.g. 'T05DP5U7M8X'
  name: string;         // e.g. 'My Company'
  url: string;          // e.g. 'https://app.slack.com/client/T05DP5U7M8X'
  iconUrl: string;      // 88×88 workspace icon
  memberCount: number;
  status: 'joined' | 'pending-invite' | 'needs-login';
  isLastActive?: boolean;
  slug: string;         // e.g. 'mycompany' from mycompany.slack.com
  userId: string | null; // current user's ID in this workspace
}
```

Each workspace has a `status` field:
- `'joined'` — active member, ready to use
- `'needs-login'` — session expired, needs re-login in browser
- `'pending-invite'` — not yet accepted invitation

### `slack.getClient(teamId?: string): Promise<WebClient>`

Extract credentials and return a fully configured `@slack/web-api` WebClient.
Opens a temporary Slack tab to read the xoxc- token from localStorage, then closes it.
If `teamId` is omitted, uses the last active workspace.

The returned `WebClient` is the standard `@slack/web-api` SDK - it has all the methods and parameters as documented in the Slack API docs.
If you have struggle using the correct API, please search `https://docs.slack.dev/reference` for the correct method and parameters.

## `filesUploadV2`

Upload single or multiple files with `client.filesUploadV2`. Accepts `file` (path, Buffer, or ReadStream) or `content` (string).

```js
// Single file
await client.filesUploadV2({
  channel_id: 'C0ARUCEK04A',
  file: './logo.png',
  filename: 'logo.png',
  initial_comment: 'New logo',
});

```


## Workspace Type
