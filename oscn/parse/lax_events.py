import json
from selectolax.parser import HTMLParser
from ._helpers import lists2dict, clean_string, MetaList

def parse_json_events(json_string):
    try:
        # Load the entire JSON data
        data = json.loads(json_string)
        # Extract events if they are in the expected structure
        if "events" in data:
            return data["events"]
    except json.JSONDecodeError:
        # Handle cases where JSON might not be properly formatted
        return []
    return []

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
        return parse_json_events(json_script.text())

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
        event_description_td = row.css_first('td.event_description')
        if event_description_td:
            event_font = event_description_td.css_first('font')
            if event_font:
                event_date = event_font.text().strip()
                event["date"] = event_date
            event["description"] = event_description_td.text().strip()
        events.append(event)

    return events

# add this attribute to allow it to be added to request objects
setattr(events, "target", ["Case"])
setattr(events, "_default_value", [])