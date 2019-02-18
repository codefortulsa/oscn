from bs4 import BeautifulSoup
from ._helpers import text_values, column_titles, lists2dict



def events(oscn_html):
    events = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    events_start = soup.find('h2', 'section events')
    events_table = events_start.find_next_sibling('table')
    thead = events_table.find('thead').find_all('th')
    event_keys = column_titles(thead)
    rows = events_table.find('tbody').find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        values = text_values(cells)
        event = lists2dict(event_keys, values)
        events.append(event)
    return events

setattr(events, 'target', ['Case'])
setattr(events, '_default_value', [])
