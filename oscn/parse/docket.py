from bs4 import BeautifulSoup
from ._helpers import text_values, add_properties, OSCN_Row


class DocketMinute(OSCN_Row):
    def __init__(self, properties=[], values=[]):
        self.publish = properties
        add_properties(self, properties, values)

    def __str__(self):
        return self.csv

    @property
    def csv(self):
        get_val = lambda prop: getattr(self, prop)
        public_vals = [get_val(p) for p in self.publish]
        return ','.join(public_vals)

    @property
    def header(self):
        return ','.join(self.publish)


def docket(oscn_html):
    minutes = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    docket_table = soup.find('table', 'docketlist')
    thead = docket_table.find('thead').find_all('th')
    rows = docket_table.find('tbody').find_all('tr')

    # make a lower case list of column names
    columns = [p for p in map(lambda str:str.lower(), text_values(thead))]

    for row in rows:
        cells = row.find_all('td')
        values = text_values(cells)
        minute = DocketMinute(columns, values)
        minutes.append(minute)

    # clean up blank dates
    current_date = minutes[0].date
    for m in minutes:
        if m.date:
            current_date = m.date
        else:
            m.date = current_date

    return minutes

setattr(docket, 'target', ['Case'])
