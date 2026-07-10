---
name: chrome
description: 'Read this when you need to use Chrome extension APIs: managing bookmarks, tabs, windows, tab groups, history, downloads, or top sites.'
icon: https://static.asidehq.com/apps/builtin-skills/chrome.svg
---
# Chrome MV3 APIs

Use the `chrome` global in the REPL. It exposes whitelisted Chrome MV3 methods with the same method names and positional arguments as extension code.

```js
const tabs = await chrome.tabs.query({});
const bookmark = await chrome.bookmarks.create({ title: 'Aside', url: 'https://aside.com' });
```

Only methods listed in this skill are callable. Use Asidewright (`page`, `locator`, `snapshot`, `openTab`) for page interaction; use `chrome.*` for browser-profile state such as bookmarks, tabs, windows, history, downloads, and top sites.

## References

- Bookmarks: read `./bookmarks.md`
- Tabs: read `./tabs.md`
- Windows: read `./windows.md`
- Tab groups: read `./tab-groups.md`
- History: read `./history.md`
- Downloads: read `./downloads.md`
- Top sites: read `./top-sites.md`
