---
name: aside-x-twitter
description: >-
  Read this skill when you need to use X (Twitter). Don't have to open a browser tab.
metadata:
  version: "0.1.0"
---
# Twitter / X

Use the `twitter` global in the REPL tool. It allows you to control the X/Twitter website with API interface- no tab open needed.

## Quick Reference

```js
// Auth check
const me = await twitter.getMe();
console.log(me); // → { id, screenName, name, description, followersCount, ... }

// Timeline (Following tab, chronological)
const timeline = await twitter.getTimeline({ count: 20 });
console.log(timeline.tweets.map(t => `@${t.author.screenName}: ${t.text.slice(0, 80)}`));

// Search
const results = await twitter.search('AI agents', { count: 20, product: 'Latest' });
console.log(results.tweets);

// Get a specific tweet
const tweet = await twitter.getTweet('1234567890');
console.log(tweet);

// Get the visible same-author thread from a tweet page
const thread = await twitter.getTweetThread('1234567890');
console.log(thread.tweets);

// Get user profile
const user = await twitter.getUser('steipete');
console.log(user);

// Post a tweet
const posted = await twitter.tweet('Hello from Aside!');
console.log(posted.id);

// Reply to a tweet
const reply = await twitter.reply('1234567890', 'Great thread!');

// Interactions
await twitter.like('1234567890');
await twitter.retweet('1234567890');
await twitter.bookmark('1234567890');

// Follow/unfollow (requires user ID, not handle)
await twitter.follow('123456');
await twitter.unfollow('123456');

// DMs
const inbox = await twitter.getDmInbox();
console.log(inbox.conversations);
const history = await twitter.getDmConversation('123-456');
console.log(history.messages);
await twitter.sendDm('123456', 'Hello!');

// Block/Mute
await twitter.block('123456');
await twitter.mute('123456');

// Notifications
const notifs = await twitter.getNotifications({ count: 10 });
console.log(notifs.notifications);
```

## Methods

### `twitter.getMe(): Promise<XUser>`

Get the authenticated user's profile.

### `twitter.getUser(screenName: string): Promise<XUser>`

Get a user profile by screen name (handle, without @).

### `twitter.getTweet(tweetId: string): Promise<XTweet>`

Get a single tweet by ID.

### `twitter.getTweetThread(tweetId: string): Promise<XTimelineResponse>`

Get the focal tweet plus visible same-author replies in the thread. Use this for X status pages when the user asks what the current page/thread is about.

### `twitter.getTimeline(opts?): Promise<XTimelineResponse>`

Get home timeline (Following tab, chronological).

- `opts.count` — Number of tweets (default `20`).
- `opts.cursor` — Pagination cursor from previous response's `nextCursor`.

### `twitter.search(query: string, opts?): Promise<XTimelineResponse>`

Search tweets.

- `query` — Search query (supports X search operators like `from:user`, `to:user`, `since:2026-01-01`).
- `opts.count` — Number of results (default `20`).
- `opts.product` — `'Latest'` (default), `'Top'`, `'People'`, `'Photos'`, `'Videos'`.
- `opts.cursor` — Pagination cursor.

### `twitter.getUserTweets(screenName: string, opts?): Promise<XTimelineResponse>`

Get a user's tweets by screen name.

- `opts.count` — Number of tweets (default `20`).
- `opts.cursor` — Pagination cursor.

### `twitter.getBookmarks(opts?): Promise<XTimelineResponse>`

Get bookmarked tweets.

### `twitter.tweet(text: string, opts?): Promise<XTweet>`

Post a new tweet. Returns the created tweet.

- `opts.mediaIds` — Array of media IDs (from media upload) to attach.

### `twitter.reply(tweetId: string, text: string, opts?): Promise<XTweet>`

Reply to a tweet. Returns the reply.

### `twitter.deleteTweet(tweetId: string): Promise<void>`

### `twitter.like(tweetId: string): Promise<void>`

### `twitter.unlike(tweetId: string): Promise<void>`

### `twitter.retweet(tweetId: string): Promise<void>`

### `twitter.unretweet(tweetId: string): Promise<void>`

### `twitter.bookmark(tweetId: string): Promise<void>`

### `twitter.unbookmark(tweetId: string): Promise<void>`

### `twitter.follow(userId: string): Promise<void>`

Follow by user ID. Get user ID from `twitter.getUser(screenName).id`.

### `twitter.unfollow(userId: string): Promise<void>`

Unfollow by user ID.

### `twitter.getDmInbox(): Promise<XDmInbox>`

Get DM inbox (list of conversations with last message preview).

### `twitter.getDmConversation(conversationId: string, opts?): Promise<XDmHistory>`

Get messages in a DM conversation. Conversation ID format: `"{lowerUserId}-{higherUserId}"`.

- `opts.maxId` — Pagination cursor for older messages (from `nextCursor`).

### `twitter.sendDm(userId: string, text: string, opts?): Promise<any>`

Send a DM to a user by their user ID. Conversation ID is auto-constructed.

- `opts.mediaId` — Attach media (from media upload).
- `opts.replyToId` — Reply to a specific message.

### `twitter.block(userId: string): Promise<void>`

### `twitter.unblock(userId: string): Promise<void>`

### `twitter.mute(userId: string): Promise<void>`

### `twitter.unmute(userId: string): Promise<void>`

### `twitter.getNotifications(opts?): Promise<{ notifications: XNotification[]; nextCursor?: string }>`

Get recent notifications.

- `opts.count` — Number of notifications (default `20`).
- `opts.cursor` — Pagination cursor.

## Types

```ts
interface XUser {
  id: string;
  screenName: string;
  name: string;
  description: string;
  followersCount: number;
  followingCount: number;
  tweetCount: number;
  profileImageUrl: string;
  isBlueVerified: boolean;
}

interface XTweet {
  id: string;
  text: string;
  author: XUser;
  createdAt: Date;
  likes: number;
  retweets: number;
  replies: number;
  bookmarks: number;
  views: number;
  media: XMedia[];
  inReplyToId?: string;
  quotedTweet?: XTweet;
}

interface XMedia {
  type: 'photo' | 'video' | 'animated_gif';
  url: string;
  width: number;
  height: number;
}

interface XTimelineResponse {
  tweets: XTweet[];
  nextCursor?: string; // pass as opts.cursor for next page
}

interface XDmMessage {
  id: string;
  text: string;
  senderId: string;
  recipientId: string;
  createdAt: Date;
  mediaUrl?: string;
}

interface XDmConversation {
  conversationId: string;
  participants: string[]; // user IDs
  lastMessage?: XDmMessage;
}

interface XDmInbox { conversations: XDmConversation[] }
interface XDmHistory { messages: XDmMessage[]; nextCursor?: string }

interface XNotification {
  id: string;
  type: string;
  timestamp: Date;
  message: string;
  raw: any;
}
```
