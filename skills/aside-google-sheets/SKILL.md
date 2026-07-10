---
name: aside-google-sheets
description: >-
  Read this skill when you need to read or write Google Sheets. Works without opening a browser tab for reads.
metadata:
  version: "0.1.0"
---
# Google Sheets

Use the `googleSheets` global in the REPL tool. Cookie-only reads work without opening a tab; write operations open a Sheets tab automatically.

IMPORTANT: User may use multiple Google accounts. ALWAYS CALL `console.log(await googleAccounts.list())` to identify the correct account UID when constructing URLs with `/u/{uid}/`.

## Quick Reference

```js
// Read spreadsheet metadata (cookie-only, no tab)
const info = await googleSheets.getSpreadsheetInfo('https://docs.google.com/spreadsheets/d/.../edit#gid=0');
console.log(info);
// → { docTitle: string, sheets: [{ name, gid, gridId, size: { rows, cols } }] }

// Read a single sheet (cookie-only, no tab)
const data = await googleSheets.readSheet('https://docs.google.com/spreadsheets/d/.../edit#gid=0');
console.log(data.cells.slice(0, 20));

// Read all sheets (cookie-only, no tab)
const allSheets = await googleSheets.readAllSheets(url);

// Write values (opens tab, clipboard paste)
await googleSheets.connect(url);
await googleSheets.writeMatrix('A1', [['Hello', 'World'], [1, 2]]);
await googleSheets.dispose();

// Navigate, notes, comments (opens tab)
await googleSheets.connect(url);
await googleSheets.navigateToCell('B5');
await googleSheets.setNote('A1', 'Remember to update');
await googleSheets.addComment('A1', 'Needs review');
await googleSheets.dispose();
```

## Methods

### Cookie-only operations (no tab needed)

#### `googleSheets.getSpreadsheetInfo(url): Promise<SpreadsheetInfo>`

Discover all sheets in a spreadsheet: names, gids, sizes.

#### `googleSheets.readSheet(url, gid?): Promise<SheetData>`

Read cell data from a specific sheet. Returns cells with values, formulas, formatting, notes, hyperlinks, images, merges, and dropdowns.

#### `googleSheets.readAllSheets(url): Promise<SheetData[]>`

Read ALL sheets in a spreadsheet. Fetches each sheet page separately.

### Tab-based operations (opens browser tab)

Call `connect(url)` before using these, and `dispose()` when done.

#### `googleSheets.connect(url): Promise<void>`

Open a Sheets tab and wait for the editor to load.

#### `googleSheets.dispose(): Promise<void>`

Close the Sheets tab.

#### `googleSheets.writeMatrix(range, data): Promise<void>`

Write a 2D array via clipboard paste. `range` is A1 notation (e.g. `'A1'`).

#### `googleSheets.writeTsv(range, tsv): Promise<void>`

Write TSV string via clipboard paste.

#### `googleSheets.writeHtml(range, html): Promise<void>`

Paste HTML content preserving rich formatting.

#### `googleSheets.navigateToCell(cell): Promise<void>`

Navigate the active cell to the given A1 address.

#### `googleSheets.switchSheet(gid): Promise<void>`

Switch to a different sheet tab by gid.

#### `googleSheets.setNote(cell, text): Promise<void>`

Set a note on a cell. Pass empty string to clear.

#### `googleSheets.addComment(cell, text): Promise<void>`

Add a threaded comment on a cell.

#### `googleSheets.readSelection(): Promise<SelectionData>`

Read current selection via copy event capture.

#### `googleSheets.readSheetRich(gid?): Promise<ExtractedCell[]>`

Read cell data with full format info from the open tab.

## Types

```ts
interface SpreadsheetInfo {
  docTitle: string;
  sheets: SheetInfo[];
}

interface SheetInfo {
  name: string;
  gid: string;
  gridId: string;
  size: { rows: number; cols: number };
}

interface SheetData extends SheetInfo {
  cells: ExtractedCell[];
}

interface ExtractedCell {
  cell: string;        // A1 notation, e.g. "B3"
  row: number;         // 1-indexed
  col: number;         // 0-indexed
  colLetter: string;
  value?: string | number | boolean;
  valueType: 'string' | 'number' | 'boolean' | 'formula' | 'image' | 'empty';
  formula?: string;    // e.g. "=SUM(A1:A10)"
  note?: string;
  hyperlink?: string;
  imageKey?: string;
  isMerged?: true;
  mergedSize?: number;
  format?: CellFormat;
  conditionalFormats?: ConditionalFormatRule[];
  dropdownOptions?: string[];
}
```

## Useful shortcuts (when tab is open)

- Jump to range: `Cmd+J`
- Select all: `Cmd+A`
- Bold / italic / underline: `Cmd+B`, `Cmd+I`, `Cmd+U`
- Comment: `Cmd+Alt+M`
- New sheet: `Shift+F11`
