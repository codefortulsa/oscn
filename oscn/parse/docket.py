from bs4 import BeautifulSoup
from ._helpers import text_values, add_properties

class DocketEvent(object):
    def __init__(self):
        pass


def docket(oscn_html):
    events = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    docket_table = soup.find('table', 'docketlist')
    thead = docket_table.find('thead').find_all('th')
    rows = docket_table.find('tbody').find_all('tr')
    headings = text_values(thead)

    for row in rows:
        cells=row.find_all('td')
        values = text_values(cells)
        event = DocketEvent()
        add_properties(event, headings, values)
        events.append(event)

        # clean up blank dates
        current_date = events[0].Date
        for e in events:
            if e.Date:
                current_date = e.Date
            else:
                e.Date = current_date

    return events

setattr(docket,'target',['OSCNrequest'])
