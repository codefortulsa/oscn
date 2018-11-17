from bs4 import BeautifulSoup
from ._helpers import text_values, lists2dict


def docket(oscn_html):
    soup = BeautifulSoup(oscn_html, 'html.parser')
    docket_table = soup.find('table', 'docketlist')
    thead = docket_table.find('thead').find_all('th')
    rows = docket_table.find('tbody').find_all('tr')
    minutes = []
    # make a lower case list of column headers
    columns = [hdr for hdr in map(lambda str:str.lower(), text_values(thead))]

    for row in rows:
        cells = row.find_all('td')
        values = text_values(cells)
        minute = lists2dict(columns, values)
        minutes.append(minute)

    # clean up blank dates
    def dt_chk(min):
        dt_chk.saved_date = min['date'] if min['date'] else dt_chk.saved_date
        min['date'] = dt_chk.saved_date
        return min

    return [dt_chk(min) for min in minutes]

setattr(docket, 'target', ['Case'])
setattr(docket, '_default_value', [])
