# Tabs API

Use `chrome.tabs.*` for tab strip state. Prefer `openTab`, `closeTab`, and `page` for normal browsing; use this API when the task is about Chrome tabs themselves.

## Methods

### `chrome.tabs.query(queryInfo)`

- `queryInfo: { active?: boolean; currentWindow?: boolean; windowId?: number; url?: string | string[]; title?: string; pinned?: boolean; audible?: boolean; discarded?: boolean; groupId?: number; index?: number }`

### `chrome.tabs.get(tabId)`

- `tabId: number`

### `chrome.tabs.create(createProperties)`

- `createProperties: { url?: string; active?: boolean; pinned?: boolean; windowId?: number; index?: number; openerTabId?: number }`

### `chrome.tabs.update(tabId?, updateProperties)`

- `tabId?: number`
- `updateProperties: { url?: string; active?: boolean; highlighted?: boolean; pinned?: boolean; muted?: boolean; openerTabId?: number; autoDiscardable?: boolean }`

### `chrome.tabs.remove(tabIds)`

- `tabIds: number | number[]`

### `chrome.tabs.reload(tabId?, reloadProperties?)`

- `tabId?: number`
- `reloadProperties?: { bypassCache?: boolean }`

### `chrome.tabs.move(tabIds, moveProperties)`

- `tabIds: number | number[]`
- `moveProperties: { windowId?: number; index: number }`

### `chrome.tabs.duplicate(tabId)`

- `tabId: number`

### `chrome.tabs.group(options)`

- `options: { tabIds: number | number[]; groupId?: number; createProperties?: { windowId?: number } }`

### `chrome.tabs.ungroup(tabIds)`

- `tabIds: number | number[]`

### `chrome.tabs.goBack(tabId?)`

- `tabId?: number`

### `chrome.tabs.goForward(tabId?)`

- `tabId?: number`
