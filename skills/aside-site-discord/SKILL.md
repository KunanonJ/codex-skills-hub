---
name: aside-site-discord
description: >-
  Discord web app channel and message workflow guidance.
metadata:
  version: "0.1.0"
---
# Discord

## Canonical URLs

- Home and DMs: `https://discord.com/channels/@me`
- Server channel: `https://discord.com/channels/${guildId}/${channelId}`
- Invite: `https://discord.gg/${code}`
- Invite: `https://discord.com/invite/${code}`

## Working style

- Prefer the web app and reuse the signed-in session.
- For known channels or servers, jump directly to the channel URL.
- Use Quick Switcher for most navigation.
- If a direct channel URL lands incorrectly, reopen from `/channels/@me` and navigate again from there.

## Useful shortcuts

- Quick switcher: `Cmd/Ctrl+K`
- Quick switcher prefixes: `*` for servers, `@` for DMs, `#` for text channels, `!` for voice channels
- Jump between major sections: `F6`, `Shift+F6`
- Move focus back to chat bar: `Escape`
- Reply to focused message: `r`
- Edit focused message: `e`
- Delete focused message: `Backspace`
- Pin focused message: `p`
- Add reaction: `+`
- Quote focused message: `q`
- Copy message content: `Cmd/Ctrl+C`
