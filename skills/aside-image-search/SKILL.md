---
name: aside-image-search
description: >-
  Use when you need to search images
metadata:
  version: "0.1.0"
---
# Image Search

Use the `imageSearch` global in the REPL tool. It fetches Google Images with the browser profile's cookies, parses result metadata from the returned HTML, and returns compact JSON. You do not need to manually inspect the DOM.

## Quick Reference

```js
const results = await imageSearch.search('max verstappen', { limit: 10 });
console.log(JSON.stringify(results, null, 2));
// → [{ title, sourceName, pageUrl, imageUrl, thumbnailUrl, width, height, dominantColor, licensable }]
```

## Methods

### `imageSearch.search(query: string, opts?: ImageSearchOptions): Promise<ImageSearchResult[]>`

Search Google Images. Returned `imageUrl` points to the discovered original image when Google exposes it. `thumbnailUrl` points to Google's thumbnail cache. License hints from Google are not legal guarantees; verify before reuse.
Browse the Google Images page directly if the helper fails.

## Types

```ts
interface ImageSearchOptions {
  limit?: number; // max search results. (default: 20)
  safeSearch?: 'active' | 'off';
  size?: 'large' | 'medium' | 'icon';
  color?: 'black' | 'blue' | 'brown' | 'gray' | 'green' | 'orange' | 'pink' | 'purple' | 'red' | 'teal' | 'transparent' | 'white' | 'yellow';
  type?: 'animated' | 'clipart' | 'lineart';
  license?: 'creativeCommons' | 'commercial';
  time?: 'day' | 'week' | 'month' | 'year';
}

interface ImageSearchResult {
  /** Human-readable image/result title from Google or the source page. */
  title: string;
  /** Publisher or site name when Google exposes it. */
  sourceName?: string;
  /** Source page that contains the image. Open this to inspect context or attribution. */
  pageUrl: string;
  /** Best-effort original image URL. Prefer this when you need the actual image asset. */
  imageUrl?: string;
  /** Google thumbnail URL. Useful for quick preview when `imageUrl` is missing or huge. */
  thumbnailUrl?: string;
  /** Original image width in pixels when Google exposes it. */
  width?: number;
  /** Original image height in pixels when Google exposes it. */
  height?: number;
  /** Dominant CSS color from Google, useful for quick UI placeholders. Example: `rgb(192,198,224)`. */
  dominantColor?: string;
  /** Google marked the result as licensable or it came from a license-filtered search. Example: `true`. */
  licensable?: boolean;
}
```
