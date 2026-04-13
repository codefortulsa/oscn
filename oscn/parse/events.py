import re
import json
from selectolax.parser import HTMLParser
from ._helpers import lists2dict, clean_string, MetaList
from unicodedata import normalize

def _parse_events_json(json_string: str) -> list[dict] | None:
    """Try to parse the script payload as JSON and extract Events array.

    strict=False tells json.loads to allow literal control characters
    (newlines, tabs, etc.) inside string values — exactly what OSCN emits.
    """
    try:
        data = json.loads(json_string, strict=False)
        raw_events = data.get("Events") or data.get("events") or []
        result = []
        for ev in raw_events:
            date = ev.get("date") or ev.get("Date") or ""
            description = ev.get("description") or ev.get("Description") or ""
            # Collapse internal whitespace in description to match table-parsed style
            description = " ".join(description.split())
            result.append({"date": date, "description": description})
        return result if result else None
    except (json.JSONDecodeError, AttributeError, TypeError):
        return None


def _parse_events_regex(json_string: str) -> list[dict]:
    """
    Fallback: extract paired (date, description) from each event object using
    a per-object regex so date and description stay coupled and multiline
    descriptions don't cause a count mismatch.
    """
    events = []
    # Match each {...} block that looks like an event object
    object_pattern = re.compile(r'\{[^{}]*?"date"[^{}]*?\}', re.DOTALL)
    date_pattern = re.compile(r'"date"\s*:\s*"(.*?)"', re.DOTALL)
    description_pattern = re.compile(r'"description"\s*:\s*"(.*?)"', re.DOTALL)

    for obj_match in object_pattern.finditer(json_string):
        obj = obj_match.group()
        date_m = date_pattern.search(obj)
        desc_m = description_pattern.search(obj)
        if date_m:
            date = date_m.group(1)
            description = " ".join(desc_m.group(1).split()) if desc_m else ""
            events.append({"date": date, "description": description})
    return events


def get_events(json_string: str) -> list[dict]:
    json_string = normalize('NFKD', json_string)

    # Primary: real JSON parse (handles all valid and lightly-malformed payloads)
    result = _parse_events_json(json_string)
    if result is not None:
        return result

    # Fallback: per-object regex — date and description extracted together so
    # multiline descriptions never cause a count mismatch between the two lists
    return _parse_events_regex(json_string)


def column_names(events_table):
    thead = events_table.css_first('thead')
    if thead:
        return [th.text().strip().lower() for th in thead.css('th')]
    return []

def events(oscn_html):
    tree = HTMLParser(oscn_html)
    events = MetaList()
    # Extract JSON events from the script tag if present
    json_script = tree.css_first("script#json_events")
    if json_script:    
        if events := get_events(json_script.text().strip()):
            return events

    # Proceed with table extraction if JSON is not found
    events_section = tree.css_first('h2.section.events')
    if not events_section:
        return events

    # Find the events table or stop at the next section
    next_element = events_section.next
    while next_element:
        if next_element.tag == 'table':
            events_table = next_element
            break
        if next_element.tag == 'h2':
            return events
        next_element = next_element.next
    else:
        return events

    # Extract table content
    events.text = events_table.text(separator=" ")
    event_keys = column_names(events_table)
    rows = events_table.css('tbody tr')
    for row in rows:
        cells = row.css('td')
        values = [clean_string(td.text()) for td in cells]
        event = lists2dict(event_keys, values)

        # Try new format first (with class="event_description")
        event_description_td = row.css_first('td.event_description')
        if event_description_td:
            event_font = event_description_td.css_first('font')
            if event_font:
                event_date = event_font.text().strip()
                event["date"] = event_date
            event["description"] = event_description_td.text().strip()
        else:
            # Fallback to old format (first cell without class)
            if cells:
                first_cell = cells[0]
                event_font = first_cell.css_first('font')
                if event_font:
                    event_date = event_font.text().strip()
                    event["date"] = event_date
                event["description"] = clean_string(first_cell.text())

        events.append(event)

    return events

# add this attribute to allow it to be added to request objects
setattr(events, "target", ["Case"])
setattr(events, "_default_value", [])