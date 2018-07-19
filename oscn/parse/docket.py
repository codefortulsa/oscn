import re
from bs4 import BeautifulSoup

count_re = r'Count as Filed:[^A-Z]*([A-Z|\d]*),\s(.*)'


        # <th>Date</th>
        # <th>Code</th>
        # <th>Description</th>
        # <th>Count</th>
        # <th>Party</th>
        # <th>Amount</th>


def docket(oscn_html):
    events = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    docket_table = soup.find('table', 'docketlist')
    thead = docket_table.find('thead').find_all('th')
    headings=[]
    for h in thead:
        headings.append(h.text)

    rows = docket_table.find('tbody').find_all('tr')

    def Event(v,h):
        pair = {}
        pair[h]=v
        return pair

    for row in rows:
        values =[]
        cells=row.find_all('td')
        for cell in cells:
            values.append(cell.text)
        pairs = map(Event, values, headings)
        events.append([p for p in pairs])

    return events
