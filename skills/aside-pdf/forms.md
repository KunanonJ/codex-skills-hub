# PDF Form Workflow

Do not fill or inspect PDF forms inside Chromium. PDF interaction in the browser is not reliable in Aside. Use `repl` with `aside.pdf`.

## Fillable Forms

1. Inspect fields:

```js
const form1 = await aside.pdf.inspectFormFields({ filePath: './input.pdf' });
console.log(JSON.stringify(form1, null, 2));
```

2. Interpret the result by separating field meaning from entered values:

- `description`, `tooltip`, `alternate_name`, `caption`, page number, and bounds describe what the input field is for.
- `value` is only the current entered value. Missing/empty `value` means no text was entered. Checkbox `value: "Off"` means unchecked, not filled.

If the user asks what fields or input boxes are in the PDF, report the field meanings even when the current values are blank.

3. Map user-provided data to `field_id` values using `description`, `tooltip`, `alternate_name`, `caption`, page number, bounds, and visual page renders when needed.

4. Fill into a new PDF. Never overwrite the source PDF unless the user explicitly asks for that.

```js
const filled1 = await aside.pdf.fillFormFields({
  filePath: './input.pdf',
  outputPath: './artifacts/filled.pdf',
  fields: [
    { field_id: 'topmostSubform[0].Page1[0].f1_14[0]', value: 'John' },
    { field_id: 'topmostSubform[0].Page1[0].c1_1[0]', value: true }
  ]
});
console.log(JSON.stringify(filled1, null, 2));
```

5. Verify output visually:

```js
const verify1 = await aside.pdf.read({ filePath: './artifacts/filled.pdf' });
display(await fs.readFile(verify1.pages[0].path));
```

If fields are ambiguous, call `aside.pdf.read({ filePath })` and inspect the rendered page images. `read()` also writes `form_fields.json` next to the rendered page images when fields exist.

## Non-Fillable Forms

If `inspectFormFields` reports no usable fields, the PDF must be filled by adding visible text or marks at coordinates. Native `aside.pdf.fillFormFields` is not the right tool for that case.

Read `fallback.md` and use the annotation workflow there.

## Failure Handling

If native inspection, rendering, or filling fails, read `fallback.md`. Do not improvise with browser PDF UI.
