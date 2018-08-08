from bs4 import BeautifulSoup


def attorneys(oscn_html):
    attorneys_parties_list = []
    attorney_list = []
    party_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section attorneys')
    attorney_table = start.find_next_sibling('table')
    #thead = attorney_table.find('thead').find_all('th')
    rows = attorney_table.find('tbody').find_all('tr')
    attorney_party_match = []

    row_number = 0
    for row in rows:
        row_number =+ 1
        if row_number%2 == 1:
            attorney = row.td.get_text()
            #attorney_party_match.append(attorney)
            attorney_list.append(attorney)

        if row_number%2 == 0:
            row.td.get_text()
            #party = row.find('td')
            #print(party)
            #attorney_party_match.append(party)
            #attorneys_parties_list.append(attorney_party_match)
            #party_list.append(party)
    return attorney_list

# add this attribute to allow it to be added to request objects
setattr(attorneys,'target',['OSCNrequest'])
