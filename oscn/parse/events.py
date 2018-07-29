from bs4 import BeautifulSoup
from ._helpers import text_values, add_properties

class Event(object):
    def __init__(self):
        pass

def events(oscn_html):
    events = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    events_start = soup.find('h2', 'section events')
    events_table = events_start.find_next_sibling('table')
    thead = events_table.find('thead').find_all('th')
    rows = events_table.find('tbody').find_all('tr')
    headings = text_values(thead)

    for row in rows:
        cells=row.find_all('td')
        values = text_values(cells)
        event = Event()
        add_properties(event, headings, values)
        events.append(event)

    return events

setattr(events,'target',['OSCNrequest'])
