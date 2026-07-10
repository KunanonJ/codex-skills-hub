---
name: aside-site-google-slides
description: >-
  Google Slides reading and editing guidance.
metadata:
  version: "0.1.0"
---
# Google Slides

## Canonical URLs

- Search: `https://docs.google.com/presentation/u/${uid}/?q=${keyword}`
- Edit: `https://docs.google.com/presentation/u/${uid}/d/${presentationId}/edit`
- Create: `https://docs.google.com/presentation/u/${uid}/create`
- HTML view: `https://docs.google.com/presentation/u/${uid}/d/${presentationId}/htmlpresent`

## Interaction model

- Prefer HTML view for lightweight reading when it preserves enough structure.
- If HTML view is insufficient, use screenshots or CUA for visible UI that refs cannot target reliably.
- Editing should use keyboard shortcuts and CUA only when the visible editor cannot be driven with refs or locators.

If you need per-slide screenshots from a read-oriented page:

```js
await page.locator(`div.slide:nth-child(${index})`).screenshot({ type: 'jpeg', quality: 80 });
```

## Useful shortcuts

- New slide: `Cmd+M`
- Delete selected slide: `Cmd+Backspace`
- Move slide up / down: `Cmd+Up`, `Cmd+Down`
- Duplicate slide: `Cmd+D`
- Grid view: `Cmd+Alt+1`
- Hide slide: `Cmd+Shift+H`
- Bold / italic / underline: `Cmd+B`, `Cmd+I`, `Cmd+U`
- Align left / center / right: `Cmd+Shift+L`, `Cmd+Shift+C`, `Cmd+Shift+R`
- Link: `Cmd+K`
- Insert image: `Cmd+Option+I`, then `I`
- Insert table: `Cmd+Option+I`, then `T`
- Insert shape: `Cmd+Option+I`, then `S`
- Insert text box: `Cmd+Option+Shift+X`
- Presentation: `Cmd+Enter`
- Start from current slide: `Shift+Cmd+Enter`
- Command palette: `Cmd+/`
