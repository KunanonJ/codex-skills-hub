---
name: aside-draft-preview
description: >-
  Use when the user explicitly asks for drafting content.
metadata:
  version: "0.1.0"
---

# Draft Preview

Only when the user explicitly asks you to draft, rewrite, reply, post, message, tweet, schedule, or preview app-shaped content, return the JSON content in the matching code block with the matching fence. The code block content must be one JSON object matching the card fields. It will be rendered as a custom component UI in the chat.

## Gmail Draft

Example:

```gmail-draft
{
  "to": ["recipient@example.com"],
  "cc": ["optional@example.com"],
  "bcc": ["optional@example.com"],
  "subject": "Subject line",
  "body": "Draft body"
}
```

- `to`: recipient email strings.
- `cc`, `bcc`: optional recipient email strings.
- `subject`: email subject.
- `body`: email body.

## LinkedIn Message Draft

Even if you are drafting a new message, include one previous message in the draft as a context to user.

Example:

```linkedin-draft
{
  "profiles": [{ "name": "Jane Doe", "avatarUrl": "https://..." }],
  "messages": [{ "name": "Jane Doe", "timestamp": "2026-07-01T09:00:00Z", "message": "Previous message" }],
  "draft": "Reply draft"
}
```

- `profiles`: people in the thread; `avatarUrl` is matched by `name`. Find avatarUrl if possible.
- `messages`: previous messages with sender `name`, parseable `timestamp`, and `message`.
- `draft`: reply text. `body` is accepted as a fallback.

## Slack Message Draft

Example:

Even if you are drafting a new message, include one previous message in the draft as a context to user. Extract avatarUrl of user/them if possible.

```slack-draft
{
  "workspace": "Acme",
  "channel": "general",
  "profiles": [{ "name": "Jane Doe", "avatarUrl": "https://..." }],
  "messages": [{ "name": "Jane Doe", "timestamp": "2026-07-01T09:00:00Z", "message": "Previous message" }],
  "draft": "Reply draft"
}
```

- `workspace`: workspace label. Defaults to `Slack`.
- `channel`: channel name without `#`. Defaults to `channel`.
- `profiles`: people in the thread; `avatarUrl` is matched by `name`.
- `messages`: previous messages with sender `name`, parseable `timestamp`, and `message`.
- `draft`: reply text. `body` is accepted as a fallback.

## Calendar Event Draft

Example:

```calendar-event-draft
{
  "title": "Event title",
  "time": "Wed, Jul 1, 2:00 PM - 2:30 PM",
  "calendarName": "Work",
  "location": "Conference room or URL",
  "attendees": [{ "name": "Jane Doe", "email": "jane@example.com", "avatarUrl": "https://..." }],
  "description": "Calendar description",
  "draft": "Invite note",
  "reminder": "10 minutes before",
  "source": "Optional source label",
  "visibility": "Default visibility",
  "availability": "Busy"
}
```

- `title`: event title.
- `time`: human-readable event time.
- `calendarName`: calendar label. Defaults to `Calendar`.
- `color`: calendar color. Defaults to `#0b57d0`.
- `location`: optional location or meeting URL.
- `attendees`: guests with `name`, `email`, and optional `avatarUrl`.
- `description`: event description.
- `draft`: invite note. `body` is accepted as a fallback.
- `reminder`, `source`, `visibility`, `availability`: optional metadata labels.

## X Post Preview

Example:

```tweet
{
  "authorName": "Jane Doe",
  "handle": "janedoe",
  "avatarUrl": "https://...",
  "timestamp": "1h",
  "body": "Post body",
  "stats": { "replies": "1", "reposts": "2", "likes": "3", "views": "400" }
}
```

- `authorName`, `handle`, `avatarUrl`: author profile.
- `timestamp`: optional display timestamp.
- `body`: post body.
- `stats`: optional display counts for `replies`, `reposts`, `likes`, and `views`.

## X Post Draft

Example:

```x-tweet-draft
{
  "profile": { "authorName": "Jane Doe", "handle": "janedoe", "avatarUrl": "https://..." },
  "body": "Draft post body"
}
```

- `profile`: author profile. `authorName`, `handle`, and `avatarUrl` are also accepted at the top level.
- `body`: draft post body.

## LinkedIn Post Preview

Example:

```linkedin-post
{
  "authorName": "Jane Doe",
  "headline": "Founder at Acme",
  "avatarUrl": "https://...",
  "timestamp": "1h",
  "body": "Post body",
  "stats": { "reactions": "12", "comments": "3" }
}
```

- `authorName`, `headline`, `avatarUrl`: author profile.
- `timestamp`: optional display timestamp.
- `body`: post body.
- `stats`: optional display counts for `reactions` and `comments`.

## LinkedIn Post Draft

Example:

```linkedin-post-draft
{
  "profile": { "authorName": "Jane Doe", "headline": "Founder at Acme", "avatarUrl": "https://..." },
  "body": "Draft post body"
}
```

- `profile`: author profile. `authorName`, `headline`, and `avatarUrl` are also accepted at the top level.
- `body`: draft post body.

