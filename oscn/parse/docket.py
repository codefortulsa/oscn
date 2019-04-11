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
        minute['html'] = row.decode()
        minutes.append(minute)

    # clean up blank dates
    saved_date = minutes[0]['date']
    for idx, min in enumerate(minutes):
        if min['date']:
            saved_date = min['date']
        else:
            min['date'] = saved_date

    return minutes

setattr(docket, 'target', ['Case'])
setattr(docket, '_default_value', [])
