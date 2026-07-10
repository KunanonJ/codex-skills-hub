# Downloads API

Use `chrome.downloads.*` for Chrome-managed downloads.

## Methods

### `chrome.downloads.search(query)`

- `query: { query?: string[]; startedBefore?: string; startedAfter?: string; endedBefore?: string; endedAfter?: string; totalBytesGreater?: number; totalBytesLess?: number; filenameRegex?: string; urlRegex?: string; finalUrlRegex?: string; limit?: number; orderBy?: string[]; id?: number; url?: string; filename?: string; danger?: string; mime?: string; startTime?: string; endTime?: string; state?: string; paused?: boolean; error?: string; bytesReceived?: number; totalBytes?: number; fileSize?: number; exists?: boolean }`

### `chrome.downloads.download(options)`

- `options: { url: string; filename?: string; saveAs?: boolean; conflictAction?: string; headers?: Array<{ name: string; value: string }>; body?: string; method?: string }`

### `chrome.downloads.pause(downloadId)`

- `downloadId: number`

### `chrome.downloads.resume(downloadId)`

- `downloadId: number`

### `chrome.downloads.cancel(downloadId)`

- `downloadId: number`

### `chrome.downloads.erase(query)`

- Same shape as `chrome.downloads.search(query)`.
