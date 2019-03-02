from bs4 import BeautifulSoup
from ._helpers import clean_string

def attorneys(oscn_html):
    attorney_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section attorneys')
    attorney_table = None
    attorney_table = start.find_next_sibling('table')
    if attorney_table:
        rows = attorney_table.find('tbody').find_all('tr')
        for row in rows:
            row_tds = row.find_all('td')
            attorney_with_address = (
                [ clean_string(s) for s in row_tds[0].stripped_strings]
            )
            representing = (clean_string(row_tds[1].text))
            attorney_list.append(
                {'name': attorney_with_address[0],
                 'address' : attorney_with_address,
                 'representing': representing
                }
            )
    return attorney_list

# add this attribute to allow it to be added to request objects
setattr(attorneys, 'target', ['Case'])
setattr(attorneys, '_default_value', [])
