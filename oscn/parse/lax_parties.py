import urllib.parse
from selectolax.parser import HTMLParser
from ._helpers import clean_string, MetaList

def get_party_id(link):
    href = link.attributes.get("href", "")
    url = urllib.parse.urlparse(href)
    params = urllib.parse.parse_qs(url.query)
    return params.get("id", [""])[0]

def parties(oscn_html):
    party_list = MetaList()
    tree = HTMLParser(oscn_html)

    section_header = tree.css_first('h2.section.party')
    if not section_header:
        return party_list

    # Find the next paragraph or stop at the next section header
    next_element = section_header.next
    while next_element:
        if next_element.tag == 'p':
            party_paragraph = next_element
            break
        if next_element.tag == 'h2':
            return party_list
        next_element = next_element.next
    else:
        return party_list

    # Extract party links and their details
    party_links = party_paragraph.css('a')
    party_data = []
    if party_links:
        for link in party_links:
            name = clean_string(link.text())
            if name.lower() == 'and':
                continue  # Skip 'AND' entries
            party_id = get_party_id(link)
            # Find the next sibling span with the type
            sibling = link.next
            party_type = ""
            while sibling:
                if sibling.tag == 'span' and 'parties_type' in sibling.attributes.get('class', ''):
                    party_type = clean_string(sibling.text())
                    break
                sibling = sibling.next
            party_data.append((name, party_id, party_type))

        names, party_ids, party_types = zip(*party_data) if party_data else ([], [], [])
    else:
        # Handle case where there are no links but spans with name and type
        spans = party_paragraph.css('span.parties_partyname, span.parties_type')
        party_data = {}
        current_name = ""
        for span in spans:
            span_class = span.attributes.get('class', '')
            if 'parties_partyname' in span_class:
                current_name = clean_string(span.text())
                if current_name.lower() == 'and':
                    continue  # Skip 'AND' entries
                party_data[current_name] = {"name": current_name, "type": "", "id": ""}
            elif 'parties_type' in span_class and current_name:
                party_data[current_name]["type"] = clean_string(span.text())

        names = [party["name"] for party in party_data.values()]
        party_types = [party["type"] for party in party_data.values()]
        party_ids = [party["id"] for party in party_data.values()]

    # Create party dictionaries and add them to the list
    raw_parties = [
        {
            "name": name,
            "type": type_string,
            "id": id_param,
        }
        for name, type_string, id_param in zip(names, party_types, party_ids)
        if name
    ]
    party_list.extend(raw_parties)

    return party_list

# add this attribute to allow it to be added to request objects
setattr(parties, "target", ["Case"])
setattr(parties, "_default_value", [])