---
name: aside-site-airtable
description: >-
  Airtable base, view, and record-pane guidance.
metadata:
  version: "0.1.0"
---
# Airtable

## Canonical URLs

- Home: `https://airtable.com/`
- Workspace: `https://airtable.com/workspaces/${workspaceId}`

## Working style

- Airtable is ID-driven. Base, table, and view URLs often use IDs like `app...`, `tbl...`, and `viw...`.
- Prefer copying the current URL instead of rebuilding it from visible names.
- Shared views often use `shr...`.
- Forms often end in `/form` and support `prefill_` and `hide_` params.
- Interface pages use `app.../pag...`.
- If a direct link falls back to Home, suspect a permission or share-type mismatch first.
- Re-snapshot after opening a record or changing a view because Airtable swaps panes in place.

## Useful shortcuts

- Shortcut help: `Cmd+/`
- Base switcher: `Cmd+K`
- Table switcher: `Cmd+J`
- View switcher: `Cmd+Shift+K`
- Find: `Cmd+F` or `Cmd+G`
- Filter: `Cmd+Shift+F`
- Group: `Cmd+Shift+D`
- Sort: `Cmd+Shift+S`
- Expand active record: `Space`
- Close expanded record: `Escape`
- Expand active cell: `Shift+Space`
- Edit selected cell: `Enter` or `F2`
- Insert record below: `Shift+Enter`
- Insert record at end: `Cmd+Shift+Enter`
- Set selected date to now: `Cmd+;`
