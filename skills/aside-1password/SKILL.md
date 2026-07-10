---
name: aside-1password
description: >-
  Read this skill when the user uses 1Password.
metadata:
  version: "0.1.0"
---
# 1Password

## How to autofill

1Password autofill options appear as an iframe popover menu after focusing a form field.

1. Click the form you want to autofill.
2. Wait 500ms, up to 1 second, for the menu to appear.
3. Take a snapshot.

Then check whether the bottom of the snapshot includes `iframe [origin="1Password"]`.

1. If the iframe autofill menu is shown and it has an appropriate item for the task, use it.
2. If the iframe autofill menu is not shown, but `status: "1Password menu is available. Press down arrow to select."` is shown, 1Password is locked. Follow the unlock flow below.
3. If neither the iframe autofill menu nor the status is shown, 1Password is not available for the form.

## When 1Password is locked

Open the 1Password extension page only to unlock 1Password with Aside PWM:

`chrome-extension://aeblfdkhhhdcdjpifhhbdiojplfjncoa/popup/index.html`

Then run:

```js
await passwordManager.unlockExternalPasswordManager(page, '1password');
```

After unlocking 1Password:

1. Return to the original sign-in page.
2. Close the 1Password extension tab opened only for unlocking.
3. **IMPORTANT: Refresh the original sign-in page.** Unless you won't see the 1Password menu.
4. Click the form field again to reopen the autofill menu.
5. Continue from the 1Password menu on the original sign-in page.

Do not use the 1Password extension page as the primary place to search and autofill website logins.
Use the original sign-in page's 1Password autofill menu for website login autofill.

If Aside PWM is locked, ask the user to unlock either Aside PWM or 1Password.

If no saved 1Password unlock item is available in Aside PWM, fall back to other password manager options. Ask the user to unlock 1Password directly only as the last resort.
