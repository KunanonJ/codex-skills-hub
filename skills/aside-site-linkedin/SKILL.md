---
name: aside-site-linkedin
description: >-
  Read this when you need to use LinkedIn.
metadata:
  version: "0.1.0"
---
# LinkedIn

Use the `linkedin` global in the REPL tool. It allows you to control the LinkedIn website with API interface- no tab open needed.

## Quick Reference

```js
// Current viewer profile. Response shape is Voyager-native:
//   { data: { plainId, '*miniProfile' }, included: [MiniProfile, ...] }
const me = await linkedin.getMe();
const miniProfile = me.included?.find((item) => item.$type === 'com.linkedin.voyager.identity.shared.MiniProfile');
console.log(miniProfile?.publicIdentifier, me.data?.plainId);

// Public profile lookup (public identifier or full profile URL)
const profile = await linkedin.getProfile('johndoe');
console.log(profile.fullName, profile.headline);

// Search people / companies
const people = await linkedin.searchPeople('software engineer at openai');
console.log(people.results.map((item) => item.title));

const companies = await linkedin.searchCompanies('openai');
console.log(companies.results.map((item) => item.title));

// Company / job / posts
const company = await linkedin.getCompany('microsoft');
const job = await linkedin.getJob('4242424242');
const posts = await linkedin.getUserPosts('johndoe');

// Messaging — inbox + conversation history (paginate by timestamp, not offset)
const inbox = await linkedin.getInbox();
const convo = await linkedin.getConversation(inbox.conversations[0].threadId);
// Reply to an existing thread
await linkedin.sendMessage({ threadId: inbox.conversations[0].threadId, text: 'Hey!' });
// Start a new thread (accepts public identifiers OR profile URNs)
await linkedin.sendMessage({ recipients: ['johndoe'], text: 'Hi, nice to meet you.' });

// Connection requests
await linkedin.sendInvitation({ identifier: 'johndoe', customMessage: 'Would love to connect.' });
const received = await linkedin.getReceivedInvitations();
if (received.invitations[0]) {
  await linkedin.acceptInvitation(received.invitations[0]);
  // or: linkedin.ignoreInvitation(received.invitations[0])
}
// Withdrawing a previously-sent invitation (URN captured from sendInvitation's response)
// await linkedin.withdrawInvitation(invitationUrn);

// If LinkedIn rotates the session cookies:
linkedin.invalidateCache();
```

## Methods

### `linkedin.getMe(): Promise<object>`

Fetch the authenticated viewer from `/voyager/api/me`. Returns the raw Voyager
payload `{ data: { plainId, '*miniProfile', ... }, included: [MiniProfile, ...] }`;
the viewer's `publicIdentifier`, `firstName`, `lastName`, etc. live on the
`MiniProfile` entry inside `included`.

### `linkedin.getProfile(identifier: string): Promise<LinkedInProfile>`

Get a public profile by LinkedIn public identifier or profile URL.

```ts
interface LinkedInProfile {
  entityUrn?: string;
  publicIdentifier?: string;
  firstName?: string;
  lastName?: string;
  fullName: string;
  headline?: string;
  summary?: string;
  location?: string;
  industryName?: string;
  occupation?: string;
  profilePicture?: string;
  backgroundPicture?: string;
  experience: Array<{
    title?: string;
    companyName?: string;
    description?: string;
    location?: string;
    startDate?: string;
    endDate?: string;
  }>;
  education: Array<{
    schoolName?: string;
    degreeName?: string;
    fieldOfStudy?: string;
    startDate?: string;
    endDate?: string;
  }>;
  raw: object;
}
```

### `linkedin.searchPeople(query: string, opts?: { offset?: number, limit?: number }): Promise<LinkedInSearchResponse>`

Search people results through Voyager search.

### `linkedin.searchCompanies(query: string, opts?: { offset?: number, limit?: number }): Promise<LinkedInSearchResponse>`

Search company results through Voyager search.

```ts
interface LinkedInSearchResponse {
  paging: { offset: number; count: number; total: number };
  results: Array<{
    entityUrn: string;
    title: string;
    headline?: string;
    subline?: string;
    summary?: string;
    navigationUrl?: string;
    image?: string;
    type?: string;
    distance?: string;
  }>;
}
```

### `linkedin.getCompany(slug: string): Promise<object | undefined>`

Fetch a company by its LinkedIn public slug (for example `microsoft`).

### `linkedin.getJob(jobId: string): Promise<object>`

Fetch a job posting by numeric job ID or `urn:li:jobPosting:*`.

### `linkedin.getUserPosts(identifier: string, opts?: { start?: number, count?: number }): Promise<LinkedInPost[]>`

Fetch posts authored by a user.

```ts
interface LinkedInPost {
  urn?: string;
  postUrl?: string;
  text?: string;
  authorName?: string;
  authorHeadline?: string;
  publishedAt?: string;
  commentCount?: number;
  likeCount?: number;
  shareCount?: number;
}
```

### `linkedin.getInbox(opts?: { createdBefore?: number }): Promise<LinkedInInboxResponse>`

List the viewer's messaging inbox. LinkedIn paginates by **timestamp cursor**, not
offset: pass the previous page's `nextCreatedBefore` back in as `createdBefore` to
fetch older conversations. The response is intentionally compact: no raw Voyager dump,
just practical thread metadata plus a parsed preview of the latest message.

```ts
interface LinkedInParticipant {
  profileUrn?: string;
  profileUrl?: string;
  fullName?: string;
  headline?: string;
  distance?: string;
  verified?: boolean;
  isSelf?: true;
}

type LinkedInMessageAttachmentKind =
  | 'audio'
  | 'conversation_ad'
  | 'external_media'
  | 'file'
  | 'forwarded_message'
  | 'image'
  | 'inmail'
  | 'message_ad'
  | 'replied_message'
  | 'unavailable'
  | 'video'
  | 'video_meeting';

interface LinkedInConversationMessagePreview {
  messageId?: string;
  sender?: LinkedInParticipant;
  subject?: string;
  text?: string;
  sentAt?: string;      // ISO string
  format?: string;
  attachmentKinds: LinkedInMessageAttachmentKind[];
}

interface LinkedInConversation {
  threadId?: string;        // stable tail like "2-ABC=="
  url?: string;
  title?: string;
  conversationType?: string;
  categories: string[];
  isGroupChat?: boolean;
  isArchived?: boolean;
  createdAt?: string;       // ISO string
  lastReadAt?: string;      // ISO string
  lastActivityAt?: string;  // ISO string
  participants: LinkedInParticipant[]; // current viewer excluded
  unreadCount?: number;
  read?: boolean;
  canReply: boolean;
  lastMessage?: LinkedInConversationMessagePreview;
}

interface LinkedInInboxResponse {
  nextCreatedBefore?: number; // Pass as opts.createdBefore on next call
  conversations: LinkedInConversation[];
}
```

### `linkedin.getConversation(threadIdOrConversationUrn: string, opts?: { createdBefore?: number }): Promise<LinkedInConversationResponse>`

Fetch messages in a single thread, newest first. You can pass either the full
conversation URN or the inbox `threadId`. Same timestamp-cursor pagination.

```ts
interface LinkedInTextLink {
  url: string;
  text?: string;
}

interface LinkedInMessageAttachmentAction {
  label?: string;
  type: 'external_website' | 'human_handoff' | 'lead_gen' | 'not_interested';
  url?: string;
  leadGenFormUrn?: string;
}

interface LinkedInMessageAttachment {
  kind: LinkedInMessageAttachmentKind;
  title?: string;
  text?: string;
  url?: string;
  previewImageUrl?: string;
  mediaType?: string;
  sizeBytes?: number;
  assetUrn?: string;
  hostProfileUrn?: string;
  inmailType?: string;
  advertiserLabel?: string;
  campaignUrn?: string;
  status?: string;
  actions?: LinkedInMessageAttachmentAction[];
}

interface LinkedInMessage {
  messageId?: string;
  threadId?: string;
  sender?: LinkedInParticipant;
  subject?: string;
  text?: string;
  sentAt?: string;     // ISO string
  format?: string;
  links: LinkedInTextLink[];
  attachments: LinkedInMessageAttachment[];
}

interface LinkedInConversationResponse {
  messages: LinkedInMessage[];
  nextCreatedBefore?: number;
}
```

### `linkedin.sendMessage(opts: { threadId?: string; recipients?: string[]; text: string }): Promise<LinkedInSendMessageResult>`

Send a direct message. Provide EITHER `threadId` (reply to an existing thread)
OR `recipients` (array of public identifiers or profile URNs — starts a new thread).
Returns the new message ID plus thread identifier.

### `linkedin.subscribeMessages(onMessage, opts?: { pollIntervalMs?: number }): Promise<void>`

Poll-based subscription to new messages across all conversations. Calls `onMessage(msg,
conversation)` once per new message. Returns when the REPL run aborts. Defaults to a
20s poll interval (minimum 5s — shorter intervals trigger throttling fast). LinkedIn's
SSE `realtime/connect` endpoint requires session-bound headers that are not recoverable
from cookies alone, so polling is the idiomatic approach here.

### `linkedin.sendInvitation(opts: { identifier: string; customMessage?: string }): Promise<object>`

Send a connection request. `identifier` can be a public identifier (`johndoe`), profile
URL, or `urn:li:fsd_profile:*` URN. `customMessage` is capped at **300 characters** and
is **Premium-only** as of 2024 — free accounts that pass a note silently drop it.

### `linkedin.getReceivedInvitations(opts?: { start?: number; count?: number }): Promise<LinkedInInvitationListResponse>`

List pending invitations the viewer has received.

```ts
interface LinkedInInvitation {
  entityUrn?: string;
  invitationId?: string;
  sharedSecret?: string;    // required to accept/ignore — echo back unchanged
  type?: 'sent' | 'received';
  message?: string;
  sentAt?: number;
  counterpart: { profileUrn?: string; publicIdentifier?: string; firstName?: string; lastName?: string; headline?: string };
  raw: object;
}
```

### `linkedin.acceptInvitation(invitation: LinkedInInvitation | string, sharedSecret?: string): Promise<void>`

Accept a received invitation. Pass the invitation object from `getReceivedInvitations`
directly (it carries the required `sharedSecret`). If you pass a string URN/id, you
MUST also provide `sharedSecret` as the second argument.

### `linkedin.ignoreInvitation(invitation: LinkedInInvitation | string, sharedSecret?: string): Promise<void>`

Reject a received invitation. Same argument shape as `acceptInvitation`.

### `linkedin.withdrawInvitation(invitation: LinkedInInvitation | string): Promise<void>`

Withdraw a previously-sent invitation. Accepts an invitation URN/id string. Capture
the URN from `sendInvitation`'s response payload. **Listing sent invitations is not
currently supported by Voyager** — scrape
`https://www.linkedin.com/mynetwork/invitation-manager/sent/` via the browser tools
if you need to enumerate pending sends.

### `linkedin.invalidateCache(): void`

Clear cached LinkedIn session cookies for the current Chrome profile.

## Canonical URLs

If you have to manually open a browser tab, navigate to these URLs:

- Home: `https://www.linkedin.com/feed`
- Messaging: `https://www.linkedin.com/messaging/`
- Search: `https://www.linkedin.com/search/results/${all|people|posts|companies|products|schools}/?keywords=${query}`
- Invitations: `https://www.linkedin.com/mynetwork/invitation-manager/`
- Notifications: `https://www.linkedin.com/notifications/?filter=all`
- Sales Navigator home: `https://www.linkedin.com/sales/home`
- Sales Navigator accounts: `https://www.linkedin.com/sales/accounts/dashboard`
- Sales Navigator leads: `https://www.linkedin.com/sales/lists/people`
- Sales Navigator inbox: `https://www.linkedin.com/sales/inbox/`

## Bot detection & throttling (READ BEFORE WRITING)

LinkedIn aggressively throttles automation. The `linkedin` global already enforces a
**~1–1.75s per-request floor with jitter** per account, which is enough for *read*
traffic at interactive pace but not enough to hide bulk *write* traffic. The risk is
not just a rate-limit: sustained abuse can trigger CAPTCHA challenges, temporary
restrictions, or a permanent ban of the user's real account.

### Risk tiers

**HIGH RISK — confirm explicitly with the user, then throttle hard:**
- `sendInvitation` — LinkedIn enforces ~**100 invitations/week** as a hard cap.
  Acceptance rate below ~20% accelerates restrictions. Default to **≤15/day** and
  space them **2–5 min apart** with jitter.
- `sendMessage` to recipients the user has never messaged before (cold outreach).
  Default to **≤20/day** with **3–10 min spacing** and never send identical copy.
- `withdrawInvitation` in bulk (looks like spam cleanup; same cap applies).

**MEDIUM RISK — fine at interactive pace, throttle bulk jobs:**
- `sendMessage` replies in existing threads (warm conversations). Cap at **≤50/day**.
- `getProfile` / `searchPeople` at scale. **≤100/day** on free; **≤300/day** Premium.
- `subscribeMessages` with `pollIntervalMs < 10_000`.

**LOW RISK — ambient use is fine:**
- `getMe`, `getInbox`, `getConversation`, `getReceivedInvitations`, `getCompany`,
  `getJob`, `getUserPosts`, `searchCompanies`.

### Safe defaults

| Operation | Min spacing | Daily cap (established account) | Weekly cap |
|---|---|---|---|
| `sendInvitation` | 2–5 min | 15–25 | **80 hard** (LinkedIn: 100) |
| `sendMessage` (cold) | 3–10 min | 20–30 | — |
| `sendMessage` (reply) | 1–3 min | 40–50 | — |
| `getProfile` / search | 5–15 s | 100–150 | — |
| `subscribeMessages` poll | **≥20 s** | — | — |

Multiply caps by **0.5×** for accounts <30 days old or dormant for 2+ weeks (LinkedIn
flags "slide & spike": inactive → sudden burst is the single strongest automation
signal). Multiply by **0×** for brand-new accounts: do a week of manual-only activity
first.

### Failure signals to watch for

- HTTP `429` → back off exponentially (1s → 2s → 4s → 8s → 16s, max 5 retries), or
  honor `Retry-After` if present. After 3 consecutive 429s: stop for 1–2 hours.
- HTTP `999` → IP-level block from LinkedIn's WAF. Stop immediately, wait 45s minimum.
- HTTP `401` / `403` → session invalidated. `linkedin.invalidateCache()` is called
  automatically, but the user must re-authenticate before retrying.
- Empty `200` with no expected data, or a redirect to `/checkpoint/...` → account is
  being challenged. Stop all writes for 24–48 hours.

### Hard don'ts

- Never send identical `sendMessage` bodies in a batch — LinkedIn has message-similarity
  ML. Vary at least the greeting line.
- Never exceed 100 invitations/week, even across multiple sessions/tools.
- Never run `sendInvitation` or bulk `sendMessage` right after the user logged back in
  from a new device/IP — LinkedIn scrutinizes fresh sessions for several hours.
- Never view 100+ profiles in <30 minutes — this is the canonical scraper signature.
- Never catch and swallow `LinkedInVoyagerError` during writes: on 429/999/403 you MUST
  stop the whole batch, not retry the next item.

### When in doubt

For any loop that does >3 write operations (`sendInvitation`, cold `sendMessage`),
confirm the full list with the user first, cap at the daily limit above, and emit
progress via `replPrint` so the user can interrupt.

## Working style

- Always wait for the app shell before snapshotting after a fresh navigation.
- In the feed, scroll down and `sleep` a bit to load more posts.
- Prefer direct search, messaging, invitation, and Sales Navigator URLs over starting from the generic home feed.
- Prefer the `linkedin` REPL global for profile/search/company/job/post data before falling back to DOM scraping.
- For writes (`sendMessage`, `sendInvitation`), read the **Bot detection & throttling** section above and throttle accordingly.
