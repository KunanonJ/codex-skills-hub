import json
import sys

from pypdf import PdfReader


def count_direct_images(page) -> int:
    resources = page.get("/Resources")
    if not resources:
        return 0
    xobjects = resources.get("/XObject")
    if not xobjects:
        return 0

    count = 0
    for obj in xobjects.values():
        subtype = obj.get("/Subtype")
        if subtype == "/Image":
            count += 1
    return count


def inspect_pdf(path: str) -> dict:
    reader = PdfReader(path)
    root = reader.trailer.get("/Root", {})
    acro_form = root.get("/AcroForm")
    fields = reader.get_fields() or {}

    pages = []
    text_pages = 0
    image_pages = 0

    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        image_count = count_direct_images(page)
        has_text = bool(text)
        has_images = image_count > 0
        if has_text:
            text_pages += 1
        if has_images:
            image_pages += 1
        pages.append(
            {
                "page": index,
                "text_chars": len(text),
                "image_count": image_count,
                "has_text": has_text,
                "has_images": has_images,
            }
        )

    has_acroform = acro_form is not None
    has_xfa = bool(acro_form and acro_form.get("/XFA"))

    if has_xfa:
        kind = "xfa-form"
    elif fields:
        kind = "acroform"
    elif text_pages == 0 and image_pages > 0:
        kind = "scanned"
    elif image_pages > 0 and text_pages > 0:
        kind = "hybrid"
    else:
        kind = "text"

    return {
        "kind": kind,
        "page_count": len(reader.pages),
        "has_acroform": has_acroform,
        "has_xfa": has_xfa,
        "field_count": len(fields),
        "text_pages": text_pages,
        "image_pages": image_pages,
        "pages": pages,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: inspect_pdf.py [input pdf]")
        sys.exit(1)
    print(json.dumps(inspect_pdf(sys.argv[1]), indent=2))
