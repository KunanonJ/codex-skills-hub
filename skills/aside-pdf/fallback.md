# PDF Fallback Workflow

Use this file only when `aside.pdf` fails or cannot perform the requested operation.

Fallbacks may require Python packages, Poppler, ImageMagick, Acrobat, or aside-runtime. Prefer file-based scripts over interactive browser PDF UI.

## Scripts

Run scripts from this skill directory:

- `scripts/inspect_pdf.py <file.pdf>`: classify the PDF and inspect structure.
- `scripts/check_fillable_fields.py <file.pdf>`: check whether fillable fields exist.
- `scripts/extract_form_field_info.py <input.pdf> <field_info.json>`: extract fillable field metadata.
- `scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>`: fill AcroForm/XFA fields with Python fallback.
- `scripts/convert_pdf_to_images.py <input.pdf> <output_dir>`: render pages for visual inspection.
- `scripts/extract_form_structure.py <input.pdf> <form_structure.json>`: extract labels, lines, and checkboxes for non-fillable forms.
- `scripts/check_bounding_boxes.py <fields.json>`: validate annotation boxes before filling.
- `scripts/fill_pdf_form_with_annotations.py <input.pdf> <fields.json> <output.pdf>`: fill non-fillable forms by drawing annotations.

## Fillable Form Fallback

1. Run `python scripts/inspect_pdf.py <file.pdf>`.
2. If the PDF is `acroform` or `xfa-form`, run `python scripts/extract_form_field_info.py <input.pdf> <field_info.json>`.
3. Use `alternate_name`, `tooltip`, page, type, and bounds to map user data to fields.
4. Create `field_values.json` with `field_id`, `page`, `description`, and `value`.
5. Run `python scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>`.
6. Render and visually verify the output.

## Non-Fillable Form Fallback

1. Run `python scripts/extract_form_structure.py <input.pdf> form_structure.json`.
2. If structure extraction is useful, derive PDF-coordinate entry boxes from labels, lines, and checkboxes.
3. If structure extraction is not useful, render pages with `scripts/convert_pdf_to_images.py` and estimate coordinates visually.
4. Use cropped zoom images to refine any uncertain coordinates.
5. Create `fields.json` and validate it with `python scripts/check_bounding_boxes.py fields.json`.
6. Run `python scripts/fill_pdf_form_with_annotations.py <input.pdf> fields.json <output.pdf>`.
7. Render and visually verify the output.

## Reference

Read `reference.md` for broader Python library examples such as `pypdf`, `pdfplumber`, rendering, splitting, merging, and metadata extraction.
