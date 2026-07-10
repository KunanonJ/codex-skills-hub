---
name: aside-google-search
description: >-
  Use this when you need to search web on Google and websearch tool is not enough
metadata:
  version: "0.1.0"
---
# Google Search

Use the `googleSearch` global in the REPL tool. It fetches Google Search with the browser profile's cookies, then parses the result DOM with stable selectors verified against a live SERP. You do not need to manually inspect the results page unless parsing fails.

## Quick Reference

```js
const results = await googleSearch.search('openai', { limit: 5 });
console.log(JSON.stringify(results, null, 2));
// → [{ title, url, sourceName, publishedAtText, snippet, sitelinks }]

// Pagination
const page2 = await googleSearch.search('openai', { start: 10 });
const page3 = await googleSearch.search('openai', { start: 20 });
```

## Query Discipline

Do not run Google Search queries in parallel. Parallel query bursts can trigger CAPTCHA or bot blocks even when each individual query is valid.

Avoid patterns like:

```js
const queries = ['first query', 'second query', 'third query'];
await Promise.all(queries.map((q) => googleSearch.search(q)));
```

Also avoid firing multiple searches from loop bodies without waiting for each result before deciding the next query. Keep Google searches sequential and only issue the next query after you have inspected the previous result.

## Methods

### `googleSearch.search(query: string, opts?: GoogleSearchOptions): Promise<GoogleSearchResult[]>`

Search Google web results and return compact structured results.

- The parser prefers stable attrs observed in the live DOM:
  - result blocks: `div[data-rpos]`
  - primary title/link: first external `a[href]` that wraps an `h3`
- This intentionally avoids relying on Google's churn-heavy class names and internal `jsname` hooks.
- Pagination uses Google's `start` offset:
  - page 1 = omit `start` or use `start: 0`
  - page 2 = `start: 10`
  - page 3 = `start: 20`
- If the helper fails, open the Google Search URL directly and inspect the page.

## Types

```ts
interface GoogleSearchOptions {
  limit?: number; // max results. default: 10
  safeSearch?: 'active' | 'off';
  language?: string; // e.g. 'en', 'ko', 'ja'
  country?: string; // e.g. 'us', 'kr', 'jp'
  start?: number; // pagination offset. e.g. 10 = page 2
  time?: 'day' | 'week' | 'month' | 'year';
}

interface GoogleSearchResult {
  title: string;
  url: string;
  sourceName?: string;
  publishedAtText?: string; // e.g. '2 hours ago'
  snippet?: string;
  sitelinks?: Array<{ title: string; url: string }>;
}
```
