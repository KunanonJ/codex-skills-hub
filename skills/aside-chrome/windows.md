# Windows API

Use `chrome.windows.*` for Chrome window state.

## Methods

### `chrome.windows.get(windowId, queryOptions?)`

- `windowId: number`
- `queryOptions?: { populate?: boolean; windowTypes?: string[] }`

### `chrome.windows.getCurrent(queryOptions?)`

- `queryOptions?: { populate?: boolean; windowTypes?: string[] }`

### `chrome.windows.getLastFocused(queryOptions?)`

- `queryOptions?: { populate?: boolean; windowTypes?: string[] }`

### `chrome.windows.getAll(queryOptions?)`

- `queryOptions?: { populate?: boolean; windowTypes?: string[] }`

### `chrome.windows.create(createData?)`

- `createData?: { url?: string | string[]; tabId?: number; left?: number; top?: number; width?: number; height?: number; focused?: boolean; incognito?: boolean; type?: string; state?: string }`

### `chrome.windows.update(windowId, updateInfo)`

- `windowId: number`
- `updateInfo: { left?: number; top?: number; width?: number; height?: number; focused?: boolean; drawAttention?: boolean; state?: string }`

### `chrome.windows.remove(windowId)`

- `windowId: number`
