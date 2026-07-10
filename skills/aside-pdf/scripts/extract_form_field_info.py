import json
import re
import sys
import xml.etree.ElementTree as ET

from pypdf import PdfReader


READ_ONLY_FLAG = 1 << 0
REQUIRED_FLAG = 1 << 1
NO_EXPORT_FLAG = 1 << 2
MULTILINE_FLAG = 1 << 12
PASSWORD_FLAG = 1 << 13
FILE_SELECT_FLAG = 1 << 20
DO_NOT_SPELL_CHECK_FLAG = 1 << 22
DO_NOT_SCROLL_FLAG = 1 << 23
COMB_FLAG = 1 << 24
RICH_TEXT_FLAG = 1 << 25


def decode_alignment(value):
    if value == 1:
        return "center"
    if value == 2:
        return "right"
    return "left"


def add_common_field_flags(field_dict, field):
    flags = int(field.get("/Ff", 0) or 0)
    field_dict["read_only"] = bool(flags & READ_ONLY_FLAG)
    field_dict["required"] = bool(flags & REQUIRED_FLAG)
    field_dict["no_export"] = bool(flags & NO_EXPORT_FLAG)
    return flags


def add_text_field_constraints(field_dict, field, flags):
    max_length = field.get("/MaxLen")
    alignment = field.get("/Q")
    default_appearance = field.get("/DA")

    if max_length is not None:
        field_dict["max_length"] = int(max_length)

    field_dict["multiline"] = bool(flags & MULTILINE_FLAG)
    field_dict["comb"] = bool(flags & COMB_FLAG)
    field_dict["password"] = bool(flags & PASSWORD_FLAG)
    field_dict["file_select"] = bool(flags & FILE_SELECT_FLAG)
    field_dict["do_not_spell_check"] = bool(flags & DO_NOT_SPELL_CHECK_FLAG)
    field_dict["do_not_scroll"] = bool(flags & DO_NOT_SCROLL_FLAG)
    field_dict["rich_text"] = bool(flags & RICH_TEXT_FLAG)

    if alignment is not None:
        field_dict["alignment"] = decode_alignment(int(alignment))
    
    if default_appearance is not None:
        field_dict["default_appearance"] = str(default_appearance)


def get_full_annotation_field_id(annotation):
    components = []
    while annotation:
        field_name = annotation.get('/T')
        if field_name:
            components.append(field_name)
        annotation = annotation.get('/Parent')
    return ".".join(reversed(components)) if components else None


def make_field_dict(field, field_id):
    field_dict = {"field_id": field_id}

    # PDF spec: /TM = human-readable field label, /TU = tooltip with instructions
    alt_name = field.get("/TM")
    tooltip = field.get("/TU")
    if alt_name:
        field_dict["alternate_name"] = str(alt_name)
    if tooltip:
        field_dict["tooltip"] = str(tooltip)

    ft = field.get('/FT')
    flags = add_common_field_flags(field_dict, field)
    if ft == "/Tx":
        field_dict["type"] = "text"
        add_text_field_constraints(field_dict, field, flags)
    elif ft == "/Btn":
        field_dict["type"] = "checkbox"  
        states = field.get("/_States_", [])
        if len(states) == 2:
            if "/Off" in states:
                field_dict["checked_value"] = states[0] if states[0] != "/Off" else states[1]
                field_dict["unchecked_value"] = "/Off"
            else:
                print(f"Unexpected state values for checkbox `${field_id}`. Its checked and unchecked values may not be correct; if you're trying to check it, visually verify the results.")
                field_dict["checked_value"] = states[0]
                field_dict["unchecked_value"] = states[1]
    elif ft == "/Ch":
        field_dict["type"] = "choice"
        states = field.get("/_States_", [])
        field_dict["choice_options"] = [{
            "value": state[0],
            "text": state[1],
        } for state in states]
    else:
        field_dict["type"] = f"unknown ({ft})"
    return field_dict


def _strip_indices(field_id):
    """Strip [N] indices from AcroForm field_id to get XFA-style path.
    e.g. 'topmostSubform[0].Page1[0].f1_01[0]' → 'topmostSubform.Page1.f1_01'
    """
    return re.sub(r'\[\d+\]', '', field_id)


# ── XFA metadata extraction ─────────────────────────────────────────────────

def _extract_xfa_metadata(reader):
    """Parse XFA template XML and build a map from dotted field path → {speak, caption}.
    IRS XFA forms (e.g. f1040) store human-readable field descriptions in
    <assist><speak> and <caption><value><text> elements, not in AcroForm /TM or /TU.
    """
    try:
        xfa = reader.xfa
    except Exception:
        return {}
    if not xfa or "template" not in xfa:
        return {}

    template = xfa["template"]
    if isinstance(template, bytes):
        template = template.decode("utf-8", errors="replace")

    try:
        root = ET.fromstring(template)
    except ET.ParseError:
        return {}

    # Detect XFA namespace version dynamically (3.0, 3.3, 3.6, etc.)
    ns_match = re.search(r'\{(http://www\.xfa\.org/schema/xfa-template/[^}]+)\}', root.tag)
    if not ns_match:
        return {}
    xfa_ns = ns_match.group(1)

    def _xfa_tag(local):
        return f"{{{xfa_ns}}}{local}"

    metadata = {}

    def _walk(element, path_parts):
        tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag
        name = element.attrib.get("name")

        if tag in ("subform", "field") and name:
            current_parts = path_parts + [name]
        else:
            current_parts = path_parts

        if tag == "field" and name:
            dotted = ".".join(current_parts)
            speak = ""
            caption_text = ""

            assist_el = element.find(_xfa_tag("assist"))
            if assist_el is not None:
                speak_el = assist_el.find(_xfa_tag("speak"))
                if speak_el is not None and speak_el.text:
                    speak = speak_el.text.strip()

            caption_el = element.find(_xfa_tag("caption"))
            if caption_el is not None:
                val_el = caption_el.find(_xfa_tag("value"))
                if val_el is not None:
                    text_el = val_el.find(_xfa_tag("text"))
                    if text_el is not None and text_el.text:
                        caption_text = text_el.text.strip()

            if speak or caption_text:
                # Duplicate field names (e.g. c1_8 for filing status radio) →
                # collect all under path; first occurrence wins for a given AcroForm id.
                if dotted not in metadata:
                    metadata[dotted] = {"speak": speak, "caption": caption_text}
                else:
                    idx = 1
                    while f"{dotted}#{idx}" in metadata:
                        idx += 1
                    metadata[f"{dotted}#{idx}"] = {"speak": speak, "caption": caption_text}

        for child in element:
            _walk(child, current_parts)

    _walk(root, [])
    return metadata


def _apply_xfa_metadata(field_info_by_id, xfa_metadata):
    """Populate alternate_name/tooltip from XFA <speak>/<caption> for fields missing them."""
    if not xfa_metadata:
        return

    seen_counts = {}

    for field_id, info in field_info_by_id.items():
        if info.get("alternate_name") and info.get("tooltip"):
            continue

        stripped = _strip_indices(field_id)
        xfa_entry = xfa_metadata.get(stripped)

        if xfa_entry is None or stripped in seen_counts:
            count = seen_counts.get(stripped, 0)
            if count > 0:
                xfa_entry = xfa_metadata.get(f"{stripped}#{count}")
            seen_counts[stripped] = count + 1
        else:
            seen_counts[stripped] = 1

        if xfa_entry is None:
            continue

        # Prefer <speak> for tooltip (most descriptive), <caption> for alternate_name
        if not info.get("alternate_name"):
            caption = xfa_entry.get("caption")
            speak = xfa_entry.get("speak")
            info["alternate_name"] = caption if caption else speak
        if not info.get("tooltip") and xfa_entry.get("speak"):
            info["tooltip"] = xfa_entry["speak"]


# ── Main extraction ──────────────────────────────────────────────────────────

def get_field_info(reader: PdfReader):
    fields = reader.get_fields() or {}

    field_info_by_id = {}
    possible_radio_names = set()

    for field_id, field in fields.items():
        if field.get("/Kids"):
            if field.get("/FT") == "/Btn":
                possible_radio_names.add(field_id)
            continue
        field_info_by_id[field_id] = make_field_dict(field, field_id)


    radio_fields_by_id = {}

    for page_index, page in enumerate(reader.pages):
        annotations = page.get('/Annots', [])
        for ann in annotations:
            field_id = get_full_annotation_field_id(ann)
            if field_id in field_info_by_id:
                field_info_by_id[field_id]["page"] = page_index + 1
                field_info_by_id[field_id]["rect"] = ann.get('/Rect')
                # /TM and /TU can live on the widget annotation instead of the field
                for key, out_key in [("/TM", "alternate_name"), ("/TU", "tooltip")]:
                    if out_key not in field_info_by_id[field_id] and ann.get(key):
                        field_info_by_id[field_id][out_key] = str(ann.get(key))
            elif field_id in possible_radio_names:
                try:
                    on_values = [v for v in ann["/AP"]["/N"] if v != "/Off"]
                except KeyError:
                    continue
                if len(on_values) == 1:
                    rect = ann.get("/Rect")
                    if field_id not in radio_fields_by_id:
                        radio_fields_by_id[field_id] = {
                            "field_id": field_id,
                            "type": "radio_group",
                            "page": page_index + 1,
                            "radio_options": [],
                        }
                    radio_fields_by_id[field_id]["radio_options"].append({
                        "value": on_values[0],
                        "rect": rect,
                    })

    # Enrich with XFA metadata (IRS XFA forms store labels in XML, not AcroForm /TM|/TU)
    xfa_metadata = _extract_xfa_metadata(reader)
    _apply_xfa_metadata(field_info_by_id, xfa_metadata)

    fields_with_location = []
    for field_info in field_info_by_id.values():
        if "page" in field_info:
            fields_with_location.append(field_info)
        else:
            print(f"Unable to determine location for field id: {field_info.get('field_id')}, ignoring")

    def sort_key(f):
        if "radio_options" in f:
            rect = f["radio_options"][0]["rect"] or [0, 0, 0, 0]
        else:
            rect = f.get("rect") or [0, 0, 0, 0]
        adjusted_position = [-rect[1], rect[0]]
        return [f.get("page"), adjusted_position]
    
    sorted_fields = fields_with_location + list(radio_fields_by_id.values())
    sorted_fields.sort(key=sort_key)

    return sorted_fields


def write_field_info(pdf_path: str, json_output_path: str):
    reader = PdfReader(pdf_path)
    field_info = get_field_info(reader)
    with open(json_output_path, "w") as f:
        json.dump(field_info, f, indent=2)
    print(f"Wrote {len(field_info)} fields to {json_output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: extract_form_field_info.py [input pdf] [output json]")
        sys.exit(1)
    write_field_info(sys.argv[1], sys.argv[2])
