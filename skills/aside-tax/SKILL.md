---
name: aside-tax
description: >-
  Federal income tax reference for Tax Year 2025 -- IRS instructions, lookup guides, and fillable PDF forms.
metadata:
  version: "0.1.0"
---
# Federal Income Tax Reference (Tax Year 2025)

This skill is a Tax Year 2025 reference library for federal income tax guidance, official instructions, and fillable PDF forms.

All paths below are relative to the `dir` value in this skill's metadata header. Use `read_file` with absolute paths (e.g. `{dir}/references/quick-reference.md`) and `rg` for searching.

## Contents

- `forms/`: blank IRS PDF forms and schedules.
- `irs-instructions/`: Tax Year 2025 IRS instruction excerpts organized by form.
- `references/`: concise lookup guides and topical notes that point back to the IRS materials.

## Reading and Filling PDF Forms

For **reading** fillable PDFs (W-2, 1040, schedules, etc.), use `extract_form_field_info.py` instead of `read_file`. It returns structured field IDs, types, and values from AcroForm fields — far more reliable than raw text extraction.

```sh
python3 {dir}/../pdf/scripts/extract_form_field_info.py <path-to-pdf>
```

For **filling** PDF forms, use the fill script which writes values into AcroForm fields:

```sh
python3 {dir}/../pdf/scripts/fill_fillable_fields.py <input.pdf> <output.pdf> --fields '{"field_name": "value", ...}'
```

To discover available field names in a form before filling, run `extract_form_field_info.py` first.

## Navigation

- Start with `references/lookup-guide/overview.md` to find the right instruction set.
- If the taxpayer may be a nonresident alien, dual-status alien, J/F/M/Q visa holder, or treaty claimant, start with `references/nonresident-aliens/overview.md` before using the resident-style 1040 guides.
- Use `references/quick-reference.md` for a short list of common Tax Year 2025 thresholds.
- Prefer the form-specific IRS instruction files when both an IRS file and a reference note cover the same issue.

## Search Efficiently

```sh
rg -n "<term>" {dir}/irs-instructions {dir}/references
rg -n "Line 16|qualified dividends" {dir}/irs-instructions/f1040 {dir}/references
```

## Proactively Solicit Documents

If fulfilling the user's request requires certain tax forms or source documents, first ask them to upload the relevant materials they already have. In general, this document solicitation should occur *before* asking any clarifying or follow-up questions. No tool call is necessary; a plaintext request suffices.

## Always Use IRS Forms

When generating draft return or filing documents, always proceed by using the forms in `forms/` (or the official IRS site, if the relevant form does not exist in `forms/`). These are fillable PDFs; you should fill out the PDFs rather than generate PDFs from scratch.

## Outside Resources

Although this skill contains a very comprehensive set of resources, you are permitted to use the means available to you to consult (fetch, search, research, etc) any resources that are **not** contained herein.

## Privacy Protocol

To protect user privacy, do not include full SSNs, EINs, or other tax identifiers in text outputs. If an identifier is to be referenced in prose, include only the last 4 digits. Full identifiers may still be used when filling forms or preparing other filing artifacts.

## Offer Assistance Liberally, with Appropriate Disclaimers

If this skill is invoked, the user is requesting your assistance on a tax-related request and you should offer it liberally (up to and including generating return documents). The user is being prominently informed within the user interface that all outputs are informational and that they should triple-check any resulting artifacts. You should not hesitate to assist the user with any query related to the materials in this skill, even if the query is complex or involves deliverables. The user is aware of the limitations and risks, and you should not be afraid to help them with any aspect of their tax-related questions or tasks.

To avoid overreliance, you can additionally supplement your final responses with appropriate disclaimer text.

For instance, for a purely informational query, you might say:

> Please note that this is for reference purposes only and should not be considered tax advice. For personalized guidance, please consult a qualified tax professional.

For a more complex query involving deliverables (e.g., "do my tax return and give me the filled-out IRS PDFs"), you should faithfully service the user's request, then end with a disclaimer resembling the following (adapted as needed):

> Please note that these draft documents are provided for reference purposes only and should not be considered tax advice. Please consult a qualified tax professional before submitting any tax documents.
