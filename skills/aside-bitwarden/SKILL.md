---
name: aside-bitwarden
description: >-
  Read this skill when the user uses Bitwarden.
metadata:
  version: "0.1.0"
---
# Bitwarden

## How to autofill

Bitwarden autofill options may appear after focusing a login form field.

1. Click the form you want to autofill.
2. Wait 500ms, up to 1 second, for the Bitwarden menu, icon, or iframe to appear.
3. Take a snapshot.

Then check whether the snapshot includes a Bitwarden autofill menu or `iframe [origin="Bitwarden"]`.

1. If the Bitwarden autofill menu is shown and it has an appropriate item for the task, use it.
2. If Bitwarden asks to unlock before showing items, follow the unlock flow below.
3. If neither the Bitwarden menu nor a Bitwarden unlock prompt is shown, Bitwarden is not available for the form.

## When Bitwarden is locked

Open the Bitwarden extension page only to unlock Bitwarden with Aside PWM:

`chrome-extension://nngceckbapebfimnlniiiahkandclblb/popup/index.html`

Then run:

```js
await passwordManager.unlockExternalPasswordManager(page, 'bitwarden');
```

After unlocking Bitwarden:

1. Return to the original sign-in page.
2. Close the Bitwarden extension tab opened only for unlocking.
3. Refresh the original sign-in page if the Bitwarden menu does not reappear.
4. Click the form field again to reopen the autofill menu.
5. Continue from the Bitwarden menu on the original sign-in page.

Do not use the Bitwarden extension page as the primary place to search and autofill website logins.
Use the original sign-in page's Bitwarden autofill menu for website login autofill.

If Aside PWM is locked, ask the user to unlock either Aside PWM or Bitwarden.

If no saved Bitwarden unlock item is available in Aside PWM, fall back to other password manager options. Ask the user to unlock Bitwarden directly only as the last resort.
