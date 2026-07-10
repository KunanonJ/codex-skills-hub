---
name: aside-notion
description: >-
  Read this skill when you need to use Notion. Don't have to open a browser tab.
metadata:
  version: "0.1.0"
---
# Notion

Use the `notion` global in the REPL tool. It extracts `token_v2` from the logged-in Notion browser session — no tab navigation needed.

## Quick Reference

```js
// If multiple Notion accounts/workspaces may be logged in, inspect and select explicitly.
console.log(await notion.listAccounts());

// Get an initialized NotionClient (cached per Chrome profile).
// IMPORTANT: Use const so you can reuse the client across REPL calls.
const _notion = await notion.getClient({
  email: 'you@example.com',
  workspaceName: 'Corca',
});

// Current user info
console.log(_notion.currentUser.email, _notion.currentUser.fullName);
console.log('Space:', _notion.currentSpace.get('name'));
console.log('Plan:', _notion.currentSpace.get('subscription_tier'));

// Search pages
const results = await _notion.search({ query: 'meeting notes', isNavigableOnly: true, limit: 10 });
for (const block of results) {
  console.log(block.id, block.get('type'), block.title);
}

// Get a page by URL or ID
const page = await _notion.getBlock('https://www.notion.so/myorg/My-Page-abc123');
console.log(page.title);

// Read page as markdown (fast, local conversion, no API call)
console.log(blockToMarkdown(page));

// Append markdown to a page
await page.children.addFromMarkdown(`
## Agent update

- [x] searched the workspace
- [x] appended a section
`);

// Create a child page
const child = await page.children.addNew('page', { title: 'New Sub-page' });
await child.children.addFromMarkdown('# Hello\n\nContent here.');

// Update page title
await page.set('properties.title', [['Updated Title']]);
```

## Getting the Client

```js
// Always assign to a const for reuse across REPL calls
const _notion = await notion.getClient();
```

The returned client is `NotionClient` from `@aside/notion` — a full-featured Notion internal API client. All operations below use this client.

If the token expires or you switch accounts:
```js
notion.invalidateCache();
const refreshedNotion = await notion.getClient();
```

## Multi-account

The client initializes with the first user/workspace found. If the task depends on a specific account or workspace, list accounts first and pass explicit selectors to `getClient`.

```js
const accounts = await notion.listAccounts();
console.log(accounts);

const client = await notion.getClient({
  email: 'other@email.com',
  workspaceName: 'Corca',
});
```

## Search

```js
// Basic search
const results = await _notion.search({ query: 'project plan', limit: 20 });

// Pages only (skip inline blocks)
const pages = await _notion.search({
  query: 'project',
  isNavigableOnly: true,
  excludeTemplates: true,
  sort: { field: 'lastEdited' }, // 'relevance' | 'lastEdited' | 'created'
});

// Search within a parent page
const childIds = await _notion.searchPagesWithParent(parentPageId, 'query');
```

Search results are `Block[]` — already cached, ready to mutate.

## Read a Page

```js
const page = await _notion.getBlock(pageIdOrUrl);

// Page metadata
console.log(page.title);
console.log(page.get('type'));

// Read children
for (const child of page.children) {
  console.log(child.get('type'), child.title);
}

// Export as markdown (fast local conversion, no API call)
console.log(blockToMarkdown(page));
```

## Write Content

Before creating pages or uploading files, verify the target workspace:

```js
console.log(_notion.currentSpace.get('name'), _notion.currentSpace.get('subscription_tier'));
console.log(_notion.currentSpace.get('settings.reach_block_limit_time'));
```

If the current workspace is free or block-limited and the user asked for a subscribed/team workspace, switch to the correct workspace before writing.

### Append blocks to a page

```js
await page.children.addNew('text', { title: 'A paragraph' });
await page.children.addNew('to_do', { title: 'Ship it', checked: false });
await page.children.addNew('bulleted_list', { title: 'List item' });
```

### Append markdown to a page

```js
await page.children.addFromMarkdown(`
# Summary

- write docs
- [x] port search API

> keep the API minimal

\`\`\`ts
console.log('ship it')
\`\`\`
`);
```

Supported: headings, paragraphs, bullet/numbered lists, to-dos, quotes, code blocks, dividers, nested lists. Inline: **bold**, *italic*, ~~strike~~, `code`, links, $$equations$$.

### Create child pages

```js
const parent = await _notion.getBlock(parentPageId);
const child = await parent.children.addNew('page', { title: 'Design Doc' });
await child.children.addFromMarkdown('# Goals\n\n- keep scope tight');
```

### Update page title

```js
await page.set('properties.title', [['New Title']]);
```

### Batch writes (transaction)

```js
await _notion.runInTransaction(async () => {
  await page.set('properties.title', [['Updated']]);
  await page.children.addNew('text', { title: 'Note 1' });
  await page.children.addNew('text', { title: 'Note 2' });
});
```

## Databases (Collections)

```js
// Get a database view by URL
const view = await _notion.getCollectionView('https://www.notion.so/myorg/8511b9fc?v=8dee2a54');
const collection = view.collection;

// List rows
const rows = await collection.getRows();
for (const row of rows.toArray()) {
  console.log(await row.getProp('Name'), await row.getProp('Status'));
}

// Add a row
const newRow = await collection.addRow({
  Name: 'New task',
  Status: 'In Progress',
  'Due Date': { start: new Date('2026-05-01') },
});

// Query with filters
const query = view.buildQuery({
  filter: {
    filters: [{
      property: 'Status',
      filter: { operator: 'enum_is', value: { type: 'exact', value: 'Done' } },
    }],
    operator: 'and',
  },
  sort: [{ property: 'Due Date', direction: 'ascending' }],
});
const result = await query.execute();
```

## Delete / Move Blocks

```js
// Soft-delete
await page.remove();

// Hard-delete
await page.remove(true);

// Move
await myBlock.moveTo(targetBlock, 'after');   // 'before' | 'after' | 'first-child' | 'last-child'
```

## Uploads

When working with file/image uploads, never print `signedPutUrl`, `signedGetUrl`, upload plans, or temporary signed response files. Log only counts, booleans, block IDs, and final Notion page URLs.

## Lock / Unlock a Page

```js
await page.set('format.block_locked', true);  // lock
await page.set('format.block_locked', false); // unlock
```

## Key Types

```ts
// Search returns Block[] — each has:
block.id;           // UUID
block.get('type');   // 'page', 'text', 'to_do', etc.
block.title;         // markdown string (pages, text blocks)
block.children;      // child blocks

// Database row properties via typed accessors:
await row.getProp('Name');      // string
await row.getProp('Status');    // string | null (select)
await row.getProp('Tags');      // string[] (multi_select)
await row.getProp('Done');      // boolean (checkbox)
await row.getProp('Due Date');  // NotionDate | null
await row.getProp('Owner');     // User[]
```

## Common Mistakes

1. **Forgetting `await` on async methods** — `getClient()`, `getBlock()`, `search()`, `getProp()`, `set()`, `addNew()`, `remove()`, and `moveTo()` are all async.
2. **Using `markdownToNotion()` for block trees** — that's for inline rich text only. Use `addFromMarkdown()` for block content.
3. **Setting page title as body** — `page.title = '# Heading\nBody'` is wrong. Set title separately, strip a matching leading `# H1` from body markdown when needed, then append body via `page.children`.
4. **Not saving the client in a variable** — without `const _notion = ...`, you re-initialize every REPL call.
5. **Writing into the wrong workspace** — check `currentSpace.get('subscription_tier')` and block-limit settings before writing.
6. **Logging signed upload URLs** — signed URLs are temporary credentials. Do not print or persist them.
