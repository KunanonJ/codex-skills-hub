---
name: aside-site-google-calendar
description: >-
  Google Calendar event browsing, search, and creation guidance.
metadata:
  version: "0.1.0"
---
# Google Calendar

## Canonical URLs

- List events: `https://calendar.google.com/calendar/u/${uid}/r/${viewMode}`
- Date-specific view: append `/YYYY/MM/DD`
- Search: `https://calendar.google.com/calendar/u/${uid}/r/search?q=${keyword}`
- Create: `https://calendar.google.com/calendar/u/${uid}/r/eventedit?...`

Recommended list view:

- `agenda` is the best default for upcoming events.
- `day`, `week`, and `month` are useful when the user asks for layout-specific context.

## Event creation

Always use link: `https://calendar.google.com/calendar/u/${uid}/r/eventedit?...`
URL params:

- `text`: title
- `dates`: `start/end`
- Timed events: `YYYYMMDDTHHmmSS/YYYYMMDDTHHmmSS` for local time, or add `Z` for UTC
- All-day events: `YYYYMMDD/YYYYMMDD`
- `ctz`: timezone
- `details`: description
- `location`: location
- `add`: comma-separated attendee emails
- `recur`: RFC-5545 rule like `RRULE:FREQ=DAILY`
- `vcon`: URL or `meet`

## Working style

- Prefer direct search and event-edit URLs over menu hunting.
- Re-snapshot after opening event dialogs or editing side panes because Calendar frequently swaps views in place.

## Useful shortcuts

- `t`: today
- `j` / `k`: next or previous period
- `c`: create event
- `e`: edit selected event
- `Backspace`: delete selected event
