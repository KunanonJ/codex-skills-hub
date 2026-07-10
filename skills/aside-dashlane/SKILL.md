---
name: aside-dashlane
description: >-
  Read this skill when the user uses Dashlane.
metadata:
  version: "0.1.0"
---
# Dashlane

## How to autofill

Dashlane autofill options may appear after focusing a login form field.

1. Click the form you want to autofill.
2. Wait 500ms, up to 1 second, for the Dashlane menu, icon, or iframe to appear.
3. Take a snapshot.

Then check whether the snapshot includes a Dashlane autofill menu or `iframe [origin="Dashlane"]`.

1. If the Dashlane autofill menu is shown and it has an appropriate item for the task, use it.
2. If Dashlane asks to unlock before showing items, follow the unlock flow below.
3. If neither the Dashlane menu nor a Dashlane unlock prompt is shown, Dashlane is not available for the form.

## When Dashlane is locked

Open the Dashlane extension page only to unlock Dashlane with Aside PWM:

`chrome-extension://fdjamakpfbbddfjaooikfcpapjohcfmg/index.html`

Then run:

```js
await passwordManager.unlockExternalPasswordManager(page, 'dashlane');
```

After unlocking Dashlane:

1. Return to the original sign-in page.
2. Close the Dashlane extension tab opened only for unlocking.
3. Refresh the original sign-in page if the Dashlane menu does not reappear.
4. Click the form field again to reopen the autofill menu.
5. Continue from the Dashlane menu on the original sign-in page.

Do not use the Dashlane extension page as the primary place to search and autofill website logins.
Use the original sign-in page's Dashlane autofill menu for website login autofill.

If Aside PWM is locked, ask the user to unlock either Aside PWM or Dashlane.

If no saved Dashlane unlock item is available in Aside PWM, fall back to other password manager options. Ask the user to unlock Dashlane directly only as the last resort.
