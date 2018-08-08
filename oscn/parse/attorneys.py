from bs4 import BeautifulSoup


def attorneys(oscn_html):
    attorney_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section attorneys')
    sibling = start.next_sibling.next_sibling
    if sibling.name == "table":
        attorney_table = sibling
        rows = attorney_table.find('tbody').find_all('tr')
        for row in rows:
                attorney = row.td.get_text()
                attorney_list.append(attorney)

    return attorney_list

# add this attribute to allow it to be added to request objects
setattr(attorneys,'target',['OSCNrequest'])
