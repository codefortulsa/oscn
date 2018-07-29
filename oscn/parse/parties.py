from bs4 import BeautifulSoup


def parties(oscn_html):
    parties_list = []
    names = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section party')
    party_p = start.find_next_sibling('p')
    party_links = party_p.find_all('a')

    for link in party_links:
        names.append(link.text)
        party_p.a.extract()

    party_type = party_p.text.split(',')
    party_type.pop(0)
    types = [r.strip() for r in party_type]

    Party = lambda name,type: {'name': name, 'type': type}

    result = map(Party, names, types)

    return [r for r in result]

# add this attribute to allow it to be added to request objects
setattr(parties,'target',['OSCNrequest'])
