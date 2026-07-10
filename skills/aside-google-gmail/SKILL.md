---
name: aside-google-gmail
description: >-
  Read this skill when you need to use user's Gmail. Don't have to open a browser tab.
metadata:
  version: "0.1.0"
---
# Gmail

Use the `gmail` global in the REPL tool. It uses direct HTTP against Gmail's internal sync API — no tab navigation needed.

IMPORTANT: User may use multiple Google accounts (e.g. work email / personal email). ALWAYS CALL `await googleAccounts.print()` to print all logged-in google accounts and identify the correct `uid` before using Gmail.

- Every `gmail` method takes `uid` (the `/u/{uid}/` index) as its first argument.
  - Use browser history search and memory search to get hint about the account to use.
- If intended search results are empty, consider trying a different `uid`. Use `Promise.all` for searching multiple accounts.
- NOTE THAT threadId is different between accounts even if it refers to the same thread.

## Quick Reference

```js
const uid = 1; // uid from Google Accounts list

// Inbox and Search
const inbox = await gmail.getInbox(uid); // shorthand for search(uid, 'in:inbox')
const searchResults = await gmail.search(uid, 'from:alice@example.com subject:"meeting"');
// → { results: GmailSearchResult[], hasMore, total, nextOffset }

// Read thread (body is markdown by default)
const thread1 = await gmail.getThread(uid, 'thread-f:123456');
// → { threadId, subject, messages: GmailThreadMessage[] }

// Compose (opens tab with pre-filled fields, returns Playwright Page)
const cp1 = await gmail.openComposer(uid, { to: 'bob@example.com', subject: 'Hi', bodyHtml: '<b>Hello</b>' });

// Reply (opens inline reply in thread detail page, returns Playwright Page)
const rp1 = await gmail.openReplyComposer(uid, { threadId: 'thread-f:123456', bodyHtml: '<p>Thanks</p>' });

// Download attachment
await gmail.downloadAttachment(uid, attachment.url, 'report.pdf');
```

## Methods

### `gmail.search(uid: number, query: string, opts?: { offset?: number }): Promise<GmailSearchResponse>`

Search threads via Gmail search operators (`from:`, `to:`, `subject:`, `label:`, `before:`, `after:`, `is:`, `has:attachment`, etc.).

- `uid` — Google account index (`/u/{uid}/`).
- `query` — Gmail search query string.
- `opts.offset` — Pagination offset (default `0`). Use `nextOffset` from previous response.

Results are paginated, concise and already token-efficient; It's safe to call `console.log` to see all results.
Call `gmail.getThread` to fetch the full thread.

### `gmail.getInbox(uid: number, offset = 0): Promise<GmailSearchResponse>`

Shorthand for `gmail.search(uid, 'in:inbox', { offset })`.

### `gmail.getThread(uid: number, threadId: string, opts?: { bodyFormat?: 'raw' | 'markdown' }): Promise<GmailThread>`

Fetch full thread with all messages, including body and attachments.

- `opts.bodyFormat` — `'markdown'` (default): body converted to compact markdown. safe to read. (`'raw'`: original HTML)
- Links in markdown body is indexed like `[Some Link][3]` then `[3]: https://example.com` at the bottom. use RegEx to capture the URL according to the index.

### `gmail.openComposer(uid: number, opts: { to?: string, cc?: string, bcc?: string, subject?: string, bodyHtml?: string }): Promise<Page>`

Open a Gmail compose tab with pre-filled fields. Returns the Playwright Page object for further interaction.

- `uid` — Google account index.
- `opts.to`, `opts.cc`, `opts.bcc` — Recipients.
- `opts.subject` — Subject line.
- `opts.bodyHtml` — HTML body to inject into the compose draft.

After clicking the send button in Composer, the tab will be automatically closed by Gmail.

### `gmail.openReplyComposer(uid: number, opts: { threadId: string, mode?: 'reply' | 'replyAll', bodyHtml?: string }): Promise<Page>`

Open an inline reply composer within a thread detail page.

- `uid` — Google account index.
- `opts.threadId` — Thread to reply to.
- `opts.mode` — `'reply'` (default) or `'replyAll'` (recommended for multi-party threads).

### `gmail.openThreadDetailsPage(uid: number, threadId: string): Promise<Page>`

Open the Gmail thread detail page in a new tab.

### `gmail.downloadAttachment(uid: number, url: string, destPath: string): Promise<string>`

Download an attachment to the dest path (relative path to the session directory). Returns the resolved file path.

## Types

```ts
type Participant = { name: string; email: string; };

interface GmailSearchResult {
  threadId: string; // e.g. 'thread-f:123456'
  subject: string;
  snippet: string; // small preview text of the thread
  timestamp: Date;
  participants: Participant[];
  isUnread: boolean;
}

interface GmailSearchResponse {
  results: GmailSearchResult[];
  hasMore: boolean;
  total: number;
  nextOffset: number;
}


interface GmailThread {
  threadId: string;
  subject: string;
  messages: GmailThreadMessage[];
  raw?: string; // raw JSON when heuristic parsing has low confidence
}

interface GmailThreadMessage {
  messageId: string;      // e.g. 'msg-f:123456'
  from: Participant;
  to: Participant[];
  cc: Participant[];
  subject: string;
  snippet: string;
  timestamp: Date;
  labels: string[];
  body: string;           // HTML (raw) or markdown, depending on bodyFormat
  attachments: Array<{
    filename: string;
    mimeType: string;
    size: number;
    url: string; // needs auth — don't download directly, use gmail.downloadAttachment()
    inline: boolean; // true for inline images
  }>;
}
```

## Compose / Reply Interaction

After `openComposer` or `openReplyComposer`, interact with the returned `Page`:

```js
// Send only after verifying the compose body is non-empty.
// If the user intentionally wants an empty email, mention that explicitly.
const bodyText = await page.locator('[role=textbox][aria-label]').innerText();
if (!bodyText.trim()) throw new Error('Gmail compose body is empty; refusing to send.');
await page.locator('[data-tooltip*="Send"]').click();

// Attach file
await page.locator('input[type=file][name=Filedata]').setInputFiles('/path/to/file');

// Discard draft
await page.locator('[data-tooltip*="Discard"]').click();
```

## Mail sending rules (IMPORTANT)

- Before sending the mail, search the existing thread or history to see if you can attach to them instead of opening the new thread.
- Please gather 3-5 user's email writing examples and try to match the tones and writing styles. Say as intermediate update that you're gathering an example, not just thinking.
- Before sending, show user the email draft with a `gmail-draft` JSON code block:

\`\`\`gmail-draft
{
  "to": ["hello@example.com"],
  "cc": [],
  "bcc": [],
  "subject": "Hello world!",
  "body": "This is the draft body."
}
\`\`\`

Then continue sending unless user required the confirmation.
If user required confirmation, use Notification tool instead of ask_user_question tool.

Before clicking Send, verify the opened Gmail composer body is not empty again.
