from bs4 import BeautifulSoup


def attorneys(oscn_html):
    attorney_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section attorneys')
    attorney_table = None
    attorney_table = start.find_next_sibling('table')
    if attorney_table:
        rows = attorney_table.find('tbody').find_all('tr')
        for row in rows:
            attorney = row.td.contents[0]
            attorney = ' '.join(attorney.split())
            attorney_list.append(attorney)

    return attorney_list

# add this attribute to allow it to be added to request objects
setattr(attorneys, 'target', ['Case'])
