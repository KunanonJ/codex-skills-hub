---
name: aside-visual-browse
description: >-
  Read this when you need a coordinate fallback for visible browser UI that snapshots, refs, or locators cannot target reliably.
metadata:
  version: "0.1.0"
---

# Visual Browse

`cua` global is available in REPL.

Visual browsing is a coordinate fallback for visible browser UI that cannot be targeted reliably with `snapshot(page)`, refs, or page locators. Use it only while the task genuinely depends on visible pixels.

## When to use

- **Canvas rendered apps**: slide/document/image editors, maps, games, charts, whiteboards and simulations
- **Custom visual controls**: drag handles, sliders, drawing surfaces, crop boxes, map pins, timeline controls
- **Unstable or missing refs**: visible controls whose snapshot refs are stale, absent, obscured, or repeatedly hit the wrong target
- **Visual verification**: when DOM state is insufficient and the next action depends on what is visibly rendered

## When not to use

Do not use visual browsing for:

- reading ordinary page text
- navigation-only work
- simple buttons, links, inputs, menus, or forms with usable refs
- repeated coordinate guesses without checking the visual result

Prefer `snapshot(page)`, refs, and locators when they can target the UI reliably.

## Operating rules

- `cua` always acts on the current active `page`. Open or focus the right tab first.
- When coordinates are not already known, call `display(await cua.getVisibleScreenshot())` before acting.
- After any CUA action that changes the page, verify before the next action.
- Use `snapshot(page)` when DOM/ref state matters.
- Use `display(await cua.getVisibleScreenshot())` when visual state matters.
- Return to `snapshot(page)`, refs, or locators as soon as the visual task is done (e.g. CAPTCHA solved, canvas interaction complete, dropdown finally submitted).
- Only keep using `visual-browse` mode while the page genuinely requires pixel-level visual interaction.
- Use coordinates for pixel-only manipulation. Use refs or locators for UI controls whenever they exist.


## Recovery

- If a popup, modal, or cookie banner blocks interaction, handle that first.
- If an action does not visibly work, take a fresh screenshot before retrying.
- If the same coordinate approach fails 2-3 times, switch strategy instead of repeating.
- For layered canvas/editor surfaces, prefer coarse sidebar/tool controls over precise clicks on stacked objects.

## API

```ts
interface CUAAPI {
  /** Click at a coordinate in the current viewport. */
  click(options: {
    x: number;
    y: number;
    button?: 'left' | 'middle' | 'right'; // Mouse button: left by default
    keypress?: string[]; // Modifier keys held during the click.
  }): Promise<void>;

  /** Double click at a coordinate in the current viewport. */
  doubleClick(options: {
    x: number;
    y: number;
    keypress?: string[]; // Modifier keys held during the double click.
  }): Promise<void>;

  /** Drag from a point to a point by the provided path. */
  drag(options: {
    path: Array<{ x: number; y: number }>; // Drag path as viewport points.
    keys?: string[]; // Optional modifier keys held during the drag.
  }): Promise<void>;

  /** Capture the visible portion of the page as a base64 PNG string. */
  getVisibleScreenshot(): Promise<string>;

  /** Press control characters at the current focused element. */
  keypress(options: {
    keys: string[]; // Key combination to press.
  }): Promise<void>;

  /** Move the mouse to a point by the provided x and y coordinates. */
  move(options: {
    keys?: string[]; // Optional modifier keys held while moving.
    x: number;
    y: number;
  }): Promise<void>;

  /** Scroll by a delta from a specific viewport coordinate. */
  scroll(options: {
    keypress?: string[]; // Modifier keys held during scroll.
    scrollX: number;
    scrollY: number;
    x: number;
    y: number;
  }): Promise<void>;

  /** Type text at the current focus. */
  type(options: { text: string }): Promise<void>;
}
```
### Modifier keys

Use these values in `keypress` / `keys`: `Alt`, `Control`, `ControlOrMeta`, `Meta`, `Shift`.
`ControlOrMeta` means `Meta` on macOS and `Control` elsewhere. Aliases also work: `Cmd`, `Command`, `Ctrl`, `Option`.

## Examples

```js
display(await cua.getVisibleScreenshot());
```

```js
await cua.click({ x: 420, y: 315 });
console.log((await snapshot(page)).tree);
```

```js
await cua.drag({
  path: [
    { x: 240, y: 540 },
    { x: 320, y: 540 },
    { x: 410, y: 540 },
  ],
});
```
