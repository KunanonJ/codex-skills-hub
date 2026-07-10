---
name: aside-youtube
description: >-
  Use this skill when you need to search YouTube, read video transcripts, or inspect comments without opening YouTube manually.
metadata:
  version: "0.1.0"
---
# YouTube

Use the `youtube` global in the REPL tool. It uses direct YouTube HTTP endpoints and returns compact JSON; you do not need to inspect YouTube DOM.

## Quick Reference

```js
const search = await youtube.search('OpenAI DevDay 2025', { limit: 5 });
const videoId = search[0].videoId;

const [metadata, transcript, comments] = await Promise.all([
  youtube.getMetadata(videoId),
  youtube.getTranscript(videoId),
  youtube.getComments(videoId, { limit: 20 }),
]);
```

## Methods

### `youtube.search(query: string, opts?: YouTubeSearchOptions): Promise<YouTubeVideoSummary[]>`

Search YouTube videos.

- `query` — search query.
- `opts.limit` — max video results. Defaults to `10`.
- `opts.lang` — YouTube UI language. Defaults to `'en'`.
- `opts.region` — YouTube region. Defaults to `'US'`.

### `youtube.getMetadata(videoIdOrUrl: string, opts?: YouTubeMetadataOptions): Promise<YouTubeVideoMetadata>`

Fetch compact video metadata such as title, channel, thumbnail, duration, view count, description, publish date, and live status.

Accepts normal watch URLs, Shorts URLs, live URLs, embed URLs, `youtu.be` URLs, or raw video IDs.

### `youtube.listTranscriptLanguages(videoIdOrUrl: string): Promise<YouTubeTranscriptLanguage[]>`

List caption tracks available for a video.

### `youtube.getTranscript(videoIdOrUrl: string, opts?: { lang?: string; includeTimestamp?: boolean }): Promise<string>`

Fetch transcript text. Omit `lang` to use YouTube's default caption track for that video. Pass a language code such as `'en'` or `'ko'` when you need a specific track. By default, it returns sentence-like plain text. Pass `includeTimestamp: true` to return one line per transcript segment formatted like `[00:00 - 00:04] text`.

### `youtube.getComments(videoIdOrUrl: string, opts?: YouTubeCommentsOptions): Promise<YouTubeCommentsResponse>`

Fetch top-level comments.

- `opts.limit` — max comments. Defaults to `20`.
- `opts.continuation` — pass the previous response's `continuation` for the next page.
- `opts.lang` — YouTube UI language. Defaults to `'en'`.
- `opts.region` — YouTube region. Defaults to `'US'`.

## Types

```ts
interface YouTubeVideoSummary {
  /** YouTube video ID, e.g. "hS1YqcewH0c". */
  videoId: string;
  /** Canonical watch URL, e.g. "https://www.youtube.com/watch?v=hS1YqcewH0c". */
  url: string;
  /** Video title. */
  title: string;
  /** Channel display name when YouTube returns it. */
  channelName?: string;
  /** Largest thumbnail URL for UI previews. */
  thumbnailUrl?: string;
}

interface YouTubeVideoMetadata extends YouTubeVideoSummary {
  /** Video length in seconds when available. */
  durationSeconds?: number;
  /** Numeric view count when available. */
  viewCount?: number;
  /** Full video description when available. */
  description?: string;
  /** Publish date in YouTube's YYYY-MM-DD format, e.g. "2025-10-06". */
  publishDate?: string;
  /** True for live videos or completed livestreams marked as live content. */
  isLiveContent?: boolean;
}

interface YouTubeCommentsResponse {
  /** Source video ID. */
  videoId: string;
  comments: Array<{
    /** Direct comment URL when YouTube returns a comment ID. */
    url?: string;
    /** Comment author's display name. */
    authorName: string;
    /** Author channel URL, e.g. "https://www.youtube.com/@OpenAI". */
    authorUrl?: string;
    /** Plain comment text. */
    text: string;
    /** YouTube's relative timestamp text, e.g. "2 months ago". */
    publishedAtText?: string;
    /** YouTube's displayed like count text, e.g. "1.2K". */
    likeCountText?: string;
    /** YouTube's displayed reply count text, e.g. "12 replies". */
    replyCountText?: string;
  }>;
  /** True when a continuation token is available. */
  hasMore: boolean;
  /** Pass this to `opts.continuation` to fetch the next page. */
  continuation?: string;
}
```
