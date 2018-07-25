from bs4 import BeautifulSoup


def text_results(ResultSet):
    text_list =[]
    for el in ResultSet:
        text_list.append(el.text.strip())
    return text_list

class DocketEvent(object):
    def __init__(self):
        pass


def docket(oscn_html):
    events = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    docket_table = soup.find('table', 'docketlist')
    thead = docket_table.find('thead').find_all('th')
    rows = docket_table.find('tbody').find_all('tr')
    headings = text_results(thead)

    for row in rows:
        cells=row.find_all('td')
        values = text_results(cells)
        event = DocketEvent()

        for idx, value in enumerate(values):
            setattr(event, headings[idx], value)
        events.append(event)
        # clean up blank dates
        current_date = events[0].Date
        for e in events:
            if e.Date:
                current_date = e.Date
            else:
                e.Date = current_date

    return events
