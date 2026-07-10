---
name: aside-captcha-solver
description: >-
  Read this skill when a page has a CAPTCHA that needs solving (reCAPTCHA, Turnstile, hCaptcha, or image CAPTCHA).
metadata:
  version: "0.1.0"
---
# Solving CAPTCHAs

Use the `captcha` global in REPL. Three methods: `click`, `drag`, `readText`. All return a snapshot tree so you can verify visually.

## Checkbox CAPTCHAs

```js
// 1. Find widget bounds via snapshot / evaluate
const s = await snapshot(page);
const bounds = await page.evaluate(`(() => {
  const el = document.querySelector('iframe');
  if (!el) return null;
  const r = el.getBoundingClientRect();
  return { x: r.x, y: r.y, width: r.width, height: r.height };
})()`);

// 2. Click and check result
const tree = await captcha.click(page, bounds);
// tree = post-click snapshot — check if widget shows checkmark / "verified"
```

## Slider / Puzzle Drag CAPTCHAs

```js
// Drag from the slider handle to the target position
const tree = await captcha.drag(page, { x: 150, y: 300 }, { x: 450, y: 300 });
// tree = post-drag snapshot — check if puzzle solved

// With more granular steps for precision
const tree = await captcha.drag(page, from, to, { steps: 40 });
```

## Text / Number CAPTCHAs

```js
// OCR the CAPTCHA image region
const text = await captcha.readText(page, { x: 100, y: 200, width: 200, height: 60 });
// → "xK7m2"

// Or OCR the full page (if bounds unknown)
const text = await captcha.readText(page);

// Then fill the input
await page.locator('input').fill(text);
```

## Methods

### `captcha.click(page?, bounds): Promise<string>`
Click within bounds (left-center), wait 3s, return snapshot tree.

### `captcha.drag(page?, from, to, opts?): Promise<string>`
Drag between two viewport coordinates. `opts.steps` controls smoothness (default 20). Returns snapshot tree.

### `captcha.readText(page?, bounds?): Promise<string | null>`
Screenshot (optionally clipped to bounds), OCR via vision model, return the text.

## Tips

- CAPTCHA widgets are often inside iframes — viewport coordinates via `page.mouse.click(x, y)` reach them
- Use `annotatedScreenshot()` if you need to visually inspect the CAPTCHA state
- For image grid challenges, use `annotatedScreenshot()` + vision to identify cells, then click each one
