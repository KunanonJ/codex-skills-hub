---
name: aside-lastpass
description: >-
  Read this skill when the user uses LastPass.
metadata:
  version: "0.1.0"
---
# LastPass

## How to autofill

LastPass autofill options may appear after focusing a login form field.

1. Click the form you want to autofill.
2. Wait 500ms, up to 1 second, for the LastPass menu, icon, or iframe to appear.
3. Take a snapshot.

Then check whether the snapshot includes a LastPass autofill menu or `iframe [origin="LastPass"]`.

1. If the LastPass autofill menu is shown and it has an appropriate item for the task, use it.
2. If LastPass asks to unlock before showing items, follow the unlock flow below.
3. If neither the LastPass menu nor a LastPass unlock prompt is shown, LastPass is not available for the form.

## When LastPass is locked

Open the LastPass extension page only to unlock LastPass with Aside PWM:

`chrome-extension://hdokiejnpimakedhajhdlcegeplioahd/popup.html`

Then run:

```js
await passwordManager.unlockExternalPasswordManager(page, 'lastpass');
```

After unlocking LastPass:

1. Return to the original sign-in page.
2. Close the LastPass extension tab opened only for unlocking.
3. Refresh the original sign-in page if the LastPass menu does not reappear.
4. Click the form field again to reopen the autofill menu.
5. Continue from the LastPass menu on the original sign-in page.

Do not use the LastPass extension page as the primary place to search and autofill website logins.
Use the original sign-in page's LastPass autofill menu for website login autofill.

If Aside PWM is locked, ask the user to unlock either Aside PWM or LastPass.

If no saved LastPass unlock item is available in Aside PWM, fall back to other password manager options. Ask the user to unlock LastPass directly only as the last resort.
