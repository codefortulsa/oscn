import urllib.parse

from bs4 import BeautifulSoup

from ._helpers import clean_string, MetaList


def get_party_id(link):
    href = link["href"]
    url = urllib.parse.urlparse(href)
    params = urllib.parse.parse_qs(url.query)

    try:
        party_id = params["id"][0]
        return party_id
    except KeyError:
        return ""


def parties(oscn_html):
    names = []
    types = []
    party_ids = []

    soup = BeautifulSoup(oscn_html, "html.parser")
    start = soup.find("h2", "section party")
    party_p = start.find_next_sibling("p")
    party_links = party_p.find_all("a")
    named_parties = MetaList()
    named_parties.text = party_p.get_text(separator=" ")

    if party_links:

        names = [link.text for link in party_links]
        party_ids = [get_party_id(link) for link in party_links]
        # party_p.strings look like "name,type,name,type"
        # [1::2] starts at the 2nd position and gets every other string
        types = [t[1::] for t in [s for s in party_p.strings][1::2]]
    else:

        def get_name_and_type(string):
            # separates a line like this into name and type
            # HEFFLIN,\xa0 ASHLEY\xa0 LAUREN,\r\nRespondent'
            more_strings = string.split(",")
            # take the last item off the list
            get_type = more_strings.pop(-1)
            # put it back together
            name = ",".join(more_strings)
            return name, get_type

        for party_text in party_p.strings:
            name, party_type = get_name_and_type(party_text)
            names.append(name)
            types.append(party_type)
            party_ids.append("")

    def Party(name, type_string, id_param):
        return {
            "name": clean_string(name),
            "type": clean_string(type_string),
            "id": id_param,
        }

    raw_parties = map(Party, names, types, party_ids)

    for party in raw_parties:
        if party["name"]:
            named_parties.append(party)

    return named_parties


# add this attribute to allow it to be added to request objects
setattr(parties, "target", ["Case"])
setattr(parties, "_default_value", [])
