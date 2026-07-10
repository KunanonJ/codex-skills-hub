---
name: aside-pdf
description: >-
  Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
metadata:
  version: "0.1.0"
---

# PDF Processing Guide

## Reading PDFs

Use `repl` with `aside.pdf` API for visual inspection of PDFs.

```ts
interface PDFReadResult {
  pages: {
    /* Image path of the rendered page. */
    path: string; 
    /* Width of the rendered page. */
    width: number;
    /* Height of the rendered page. */
    height: number;
  }[];
  /** If there are form fields, it's metadata JSON path. Use `read_file` to read it. */
  formFieldsPath: string | undefined;
}

interface AsidePdf {
  /** Render PDF pages as images and inspect form fields using macOS native PDFKit. */
  read(options: { filePath: string; outputDir?: string; maxDimension?: number }): Promise<PDFReadResult>;

  /** Inspect AcroForm/XFA fields and return field descriptions when embedded in the PDF. */
  inspectFormFields(options: { filePath: string }): Promise<Record<string, unknown>>;

  /** Fill AcroForm fields into a new output PDF. */
  fillFormFields(options: {
    filePath: string;
    outputPath: string;
    fields: { field_id: string; value: boolean | number | string | null }[];
  })
}
```

## REPL Examples

```js
// Reading a PDF (pages[].path is the image path of the rendered page- use either `read_file` tool or `display(await fs.readFile(path))` to read the PDF as image)
console.log(await aside.pdf.read({ filePath: './input.pdf' }));

// Inspecting form fields
console.log(await aside.pdf.inspectFormFields({ filePath: './input.pdf' }));

// Filling form fields
await aside.pdf.fillFormFields({
  filePath: './input.pdf',
  outputPath: './artifacts/filled.pdf',
  fields: [
    { field_id: 'topmostSubform[0].Page1[0].f1_14[0]', value: 'John' },
    { field_id: 'topmostSubform[0].Page1[0].c1_1[0]', value: true }
  ]
});
```

## Notes

Do not answer "the form is empty" when the user is asking what fields exist. Report the field meanings and separately say whether current values are blank.

If `aside.pdf` fails or the native helper cannot perform the requested operation, read `fallback.md` and use the fallback workflow.


## Writing PDFs

Use `bash` tool with `node` + `pdf-lib` to write PDFs. NEVER use `repl` for `pdf-lib`- it's not available on REPL.
Please read `./reference.md` for more advanced PDF writing examples.


## IMPORTANT: Visually verify after PDF writing

- You must read the output PDF and visually verify the changes.
- Verify form/table/element positions and sizes are correct. Iterate until the output is correct.
