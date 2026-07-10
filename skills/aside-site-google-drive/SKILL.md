---
name: aside-site-google-drive
description: >-
  Google Drive navigation and result-reading guidance.
metadata:
  version: "0.1.0"
---
# Google Drive

## Canonical URLs

- My Drive: `https://drive.google.com/drive/u/${uid}/my-drive`
- Shared with me: `https://drive.google.com/drive/u/${uid}/shared-with-me`
- Recent: `https://drive.google.com/drive/u/${uid}/recent`
- Starred: `https://drive.google.com/drive/u/${uid}/starred`
- Trash: `https://drive.google.com/drive/u/${uid}/trash`
- Search: `https://drive.google.com/drive/u/${uid}/search?q=${keyword}`
- Folder: `https://drive.google.com/drive/u/${uid}/folders/${folderId}`
- File view: `https://drive.google.com/drive/file/d/${fileId}/view?authuser=${uid}`

## Search results behavior

Single click usually selects. To open a search result, double click the `gridcell`.

- Results commonly open in a dialog, not a new tab.
- After closing the dialog, take a fresh snapshot before touching the next result.

Helper for reading multiple results:

```js
const readGdriveResults = async (page, refs, action = 'snapshot', delay = 100) => {
  const results = [];
  for (const ref of refs) {
    await page.locator(ref).dblclick();
    await sleep(delay);
    if (action === 'snapshot') {
      results.push((await snapshot(page)).tree);
    } else if (action === 'screenshot') {
      results.push(await page.locator(ref).screenshot());
    }
    await page.keyboard.press('Escape');
    await snapshot(page);
  }
  return results;
};
```

## Working style

- Prefer search, folder, and direct file URLs over browsing from the Drive home surface.
- Re-snapshot after open, close, share, and move dialogs because Drive re-renders panes heavily.
