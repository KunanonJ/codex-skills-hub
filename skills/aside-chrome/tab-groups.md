# Tab Groups API

Use `chrome.tabGroups.*` for Chrome tab groups.

## Methods

### `chrome.tabGroups.query(queryInfo)`

- `queryInfo: { collapsed?: boolean; color?: string; title?: string; windowId?: number }`

### `chrome.tabGroups.get(groupId)`

- `groupId: number`

### `chrome.tabGroups.update(groupId, updateProperties)`

- `groupId: number`
- `updateProperties: { collapsed?: boolean; color?: string; title?: string }`

### `chrome.tabGroups.move(groupId, moveProperties)`

- `groupId: number`
- `moveProperties: { index: number; windowId?: number }`
