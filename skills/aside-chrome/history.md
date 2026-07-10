# History API

Use `chrome.history.*` for the user's browsing history.

## Methods

### `chrome.history.search(query)`

- `query: { text: string; startTime?: number; endTime?: number; maxResults?: number }`

### `chrome.history.getVisits(details)`

- `details: { url: string }`

### `chrome.history.addUrl(details)`

- `details: { url: string; title?: string; transition?: string }`

### `chrome.history.deleteUrl(details)`

- `details: { url: string }`

### `chrome.history.deleteRange(range)`

- `range: { startTime: number; endTime: number }`
