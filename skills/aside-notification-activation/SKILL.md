---
name: aside-notification-activation
description: >-
  Enable browser notifications on websites for monitoring and event-driven routine flows.
metadata:
  version: "0.1.0"
---
# Notification Activation

Enabling website notifications requires TWO steps — browser permission AND site-level opt-in. Both are mandatory; browser permission alone does nothing if the site hasn't been told to send notifications.

## Step 0: Check if already granted

Before granting permission, check if this origin already has a notification grant:

```js
// Query the daemon to see if we already granted notification permission for this origin
const origin = new URL(page.url()).origin;
const existing = await trpcClient.inbox.getNotificationGrant.query({ origin });
if (existing) {
  // Already granted — skip to Step 2 (site-level opt-in) or Step 3 (source resolution)
}
```

If a grant already exists, skip Step 1 entirely. The browser already has "Allow for AI" permission for this origin. Proceed to Step 2 if site-level opt-in has not been done, then Step 3 before waiting.

## Step 1: Grant browser permission

```js
await page.grantNotificationPermission();
```

Call this on the target site FIRST. This does two things:
1. Grants "Allow for AI" notification permission at the browser level (silent, no dialog)
2. Records the grant in the daemon so future sessions can check without re-granting

After `grantNotificationPermission()` returns, wait for the page to settle before proceeding to Step 2.

## Step 2: Enable notifications in the site's settings UI

This is the critical step. Most websites require you to opt in to desktop/browser/push notifications from their own settings page. The general strategy:

### 2a. Navigate to the site's notification settings

```js
// Take a snapshot to orient — look for settings/gear icons, profile menus
await snapshot(page, { interactive: true });

// Common approaches:
// 1. Direct URL if known (check browsing history or guess common patterns)
//    e.g. /settings/notifications, /preferences, /account/notifications
// 2. Click settings icon (gear) → look for "Notifications" section
// 3. Profile menu → Settings/Preferences → Notifications tab
```

### 2b. Find and enable the notification toggle

```js
// Snapshot the settings page — look for notification-related controls
await snapshot(page);

// Search for keywords in the snapshot:
// - "Desktop notifications", "Browser notifications", "Push notifications"
// - "Email notifications" (NOT this — we want push/desktop only)
// - Toggle switches, checkboxes, "Enable" / "Turn on" / "Allow" buttons
// - "New mail notifications" (Gmail-like), "Notify me about..." (Slack-like)
```

### 2c. Activate and verify

```js
// Click the toggle/checkbox/button
await page.locator('<ref>').click();

// Snapshot diff to confirm state changed
const after = await snapshot(page);
// Verify the toggle shows "on" state or a success message appeared
```

### 2d. Handle edge cases

- **"Notifications blocked" message** → Step 1 wasn't applied. Run `page.grantNotificationPermission()`, reload, retry.
- **Confirmation dialog** → Accept it.
- **Multiple notification types** → Enable "Desktop" or "Browser" or "Push" notifications specifically. Skip email/SMS toggles.
- **Nested settings** → Some sites bury notification toggles under sub-sections. Keep drilling down.
- **No notification settings found** → The site may use a notification banner/prompt on the main page instead of a settings toggle. Navigate back to the main page and look for "Enable notifications" banners.

## Step 3: Resolve the notification site before waiting

Before creating an event routine, resolve the user's site/service reference to the exact page origin. Never pass the user's raw phrase directly as `eventFilter.from`.

Resolution priority:

1. Current or most recent task tab origin for phrases like "this site", "here", "that service", or "the one I just used".
2. Recent task/conversation URLs.
3. Existing notification grants via `trpcClient.inbox.listNotificationGrants.query()`.
4. Browsing history search for the service/site name.
5. Ask a short clarification if multiple origins are plausible.

Use the technical origin URL internally, but speak to the user in site/domain terms. 
Good: "I'll wait for Gmail site notifications." or "I'll wait for notifications from mail.google.com." 
Avoid exposing implementation wording like "origin subscription" unless the user asks.

If the user wants any browser notification classified, omit `eventFilter.from` and inspect the received event after wake. For a specific named site/service, resolve the site first and use the origin URL.

## Step 4: Create an event routine for the notifications

After browser permission, site-level opt-in, and source resolution succeed, create an event routine with `routine_update`:

For a one-shot wait that continues this conversation when the notification arrives ("wake me when the Gmail reply comes"):

```
mode: "create"
kind: "heartbeat"            ← wakes this session
triggerKind: "event"
scheduleKind: "once"         ← auto-pauses after the first matching event
eventFilter: { source: "web-push-notification", from: "<origin URL>" }
timeoutMinutes: 60           ← optional; defaults to 60 for once waits
name/prompt: what to do when the event (or timeout) arrives
```

Then end the turn normally — the session stays idle and is woken with the event content when a matching notification arrives, or with a timeout notice if the deadline passes.

For a standing monitor that starts a new task per notification, use `kind: "cron"` with `scheduleKind: "recurring"` instead.

**`eventFilter.from` must be the page origin URL** (e.g. `https://mail.google.com`, `https://app.slack.com`), NOT an email address or username. This is because the browser delivers push notifications tagged with the sending origin.
