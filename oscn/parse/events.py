import json
import re

from bs4 import BeautifulSoup
from ._helpers import text_values, column_titles, lists2dict, clean_string, MetaList

event_pattern = re.compile(
    r'\{\s*"date":\s*".*?",\s*"description":\s*".*?"\s*\}', re.DOTALL
)

def get_event_dict(event_string):
    # Extract the date and description using regex
    date_match = re.search(r'"date":\s*"(.*?)"', event_string)
    description_match = re.search(r'"description":\s*"(.*?)"', event_string)

    if date_match and description_match:
        date = date_match.group(1)
        description = description_match.group(1).replace("\\", "\\\\")
        return {
            "date": date,
            "description": description
        }
    return None

def escape_description(match):
    description = match.group(2)
    escaped_description = description.replace("\\", "\\\\")
    return f'{match.group(1)}{escaped_description}{match.group(3)}'

def find_events(some_string):
    # Find all event objects using the precompiled regex pattern
    event_objects = event_pattern.findall(some_string)
    
    # Initialize list to hold cleaned events as dictionaries
    events = []

    for event in event_objects:
        # Clean up extra whitespace/newlines around the JSON object
        clean_event = re.sub(r'[\n\t\r]', '', event).strip()

        # Escape problematic characters in the description field
        clean_event = re.sub(
            r'("description":\s*")([^"]*?)(")',
            escape_description,
            clean_event
        )

        # Parse the cleaned string into a dictionary
        event_dict = get_event_dict(clean_event)
        if event_dict:
            events.append(event_dict)

    return events

def events(oscn_html):
    soup = BeautifulSoup(oscn_html, "html.parser")    
    if json_script := soup.find("script", {"id": "json_events"}):
        return find_events(json_script.string)
    
    events = MetaList()
    events_start = soup.find("h2", "section events")
    events_table = events_start.find_next_sibling()
    if events_table.name == "table":
        events.text = events_table.get_text(separator=" ")
        thead = events_table.find("thead").find_all("th")
        event_keys = column_titles(thead)
        rows = events_table.find("tbody").find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            values = text_values(cells)
            event = lists2dict(event_keys, values)
            event_font = cells[0].font.extract()
            event_date = clean_string(event_font.text)
            event["date"] = event_date
            event["description"] = clean_string(cells[0].text)
            events.append(event)
    
    return events

setattr(events, "target", ["Case"])
setattr(events, "_default_value", [])
