---
name: aside-google-docs
description: >-
  Read this skill when you need to read or write Google Docs. Reading works without opening a browser tab.
metadata:
  version: "0.1.0"
---
# Google Docs

Use the `googleDocs` global in the REPL tool. Cookie-only reads work without opening a tab; editing operations open a Docs tab automatically.

IMPORTANT: User may use multiple Google accounts. ALWAYS CALL `console.log(await googleAccounts.list())` to identify the correct account UID when constructing URLs with `/u/{uid}/`.

## Quick Reference

```js
// Parse URL to get docId and uid
const { docId, uid } = googleDocs.parseUrl('https://docs.google.com/document/u/1/d/abc123/edit');
// → { docId: 'abc123', uid: 1 }

// Read document (cookie-only, no tab needed)
const html = await googleDocs.getDocumentHTML('https://docs.google.com/document/u/1/d/.../edit');
const text = await googleDocs.getDocumentText('https://docs.google.com/document/u/1/d/.../edit');

// Or pass { docId, uid } directly
const html2 = await googleDocs.getDocumentHTML({ docId: 'abc123', uid: 1 });

// Edit document (opens tab)
await googleDocs.connect(url);
const title = await googleDocs.getTitle();
const liveText = await googleDocs.getLiveText();
await googleDocs.insertText('Hello world');
await googleDocs.dispose();

// Apply surgical diffs (the killer feature)
await googleDocs.connect(url);
await googleDocs.applyDiffs([
  { type: 'replace', startIndex: 0, endIndex: 5, text: 'Hello' },
  { type: 'insert', startIndex: 10, text: ' world' },
  { type: 'delete', startIndex: 20, endIndex: 25 },
]);
await googleDocs.dispose();

// Apply diffs as suggestions
await googleDocs.connect(url);
await googleDocs.applyDiffsAsSuggestions(diffs, 'Fixed grammar issues');
await googleDocs.dispose();
```

## Methods

### Cookie-only operations (no tab needed)

#### `googleDocs.parseUrl(url): { docId: string; uid?: number }`

Extract docId and uid from a Google Docs URL. Useful for multi-account scenarios where you need to pass `{ docId, uid }` to read methods.

#### `googleDocs.getDocumentHTML(target): Promise<string>`

Fetch the full document as HTML. `target` is a URL string or `{ docId: string; uid?: number }`. Include `/u/{uid}/` in the URL (or pass `uid`) for multi-account.

#### `googleDocs.getDocumentText(target): Promise<string>`

Fetch the full document as plain text. Same `target` signature as `getDocumentHTML`.

### Tab-based operations (opens browser tab)

Call `connect(url)` before using these, and `dispose()` when done.

#### `googleDocs.connect(url): Promise<void>`

Open a Docs tab and wait for the editor to load.

#### `googleDocs.dispose(): Promise<void>`

Close the Docs tab.

#### `googleDocs.getTitle(): Promise<string>`

Read the document title from the live editor.

#### `googleDocs.getLiveText(): Promise<string>`

Read the full document text from the live editor. Note: temporarily selects all text to read it.

#### `googleDocs.getSelectedContent(): Promise<{ text: string; html: string }>`

Read the current selection as text and HTML.

#### `googleDocs.insertText(text): Promise<void>`

Insert text at the current cursor position.

#### `googleDocs.selectAll(): Promise<void>`

Select all document text.

#### `googleDocs.selectTextRange(startIndex, endIndex): Promise<void>`

Select a range of text by character indices.

#### `googleDocs.insertHtmlContent(html): Promise<void>`

Paste rich HTML content at the cursor position.

#### `googleDocs.pasteFromMarkdown(markdown): Promise<void>`

Use Docs' "Paste from Markdown" context menu item.

#### `googleDocs.applyDiffs(diffs): Promise<void>`

Apply surgical text modifications using select-and-replace. Diffs are sorted end-to-start so later edits don't shift earlier indices.

```ts
interface TextDiff {
  type: 'replace' | 'delete' | 'insert';
  startIndex: number;
  endIndex?: number;  // required for replace and delete
  text?: string;      // required for replace and insert
}
```

#### `googleDocs.applyDiffsAsSuggestions(diffs, explanation?): Promise<void>`

Apply diffs as Google Docs suggestions. Switches to suggestion mode, applies diffs, then switches back. Optionally adds an explanation comment.

#### `googleDocs.addComment(text): Promise<void>`

Add a comment on the current selection.

#### `googleDocs.deleteSelection(): Promise<void>`

Delete the currently selected text.

## Notes

- Cookie-only reads are preferred — they're faster, lighter, and don't disturb the user's browser.
- For editing, always `connect()` → edit → `dispose()`.
- `applyDiffs()` and `applyDiffsAsSuggestions()` are the primary editing mechanisms — they're precise, index-based, and handle multiple edits atomically.
- HTML insertion works via clipboard paste — Docs decides which tags and styles survive.
- Markdown paste depends on the English "Paste from Markdown" menu label.
- Selection-by-index uses SVG rect mapping and may be less reliable after large edits.

## Useful shortcuts (when tab is open)

- Select all: `Cmd+A`
- Find: `Cmd+F`
- Find and replace: `Cmd+Shift+H`
- Comment: `Cmd+Alt+M`
- Heading 1-6: `Cmd+Alt+1` through `Cmd+Alt+6`
- Bold / italic / underline: `Cmd+B`, `Cmd+I`, `Cmd+U`
- Undo / redo: `Cmd+Z`, `Cmd+Y`
