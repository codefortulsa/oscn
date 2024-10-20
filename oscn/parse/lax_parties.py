import urllib.parse
from selectolax.parser import HTMLParser
from ._helpers import clean_string, MetaList

def get_party_info(link):
    href = link.attributes.get("href", "")
    party_id = href.split("id=")[-1] if "id=" in href else ""
    return party_id, href

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
    party_list.text = party_paragraph.text().strip()
    # Extract party details from spans within the paragraph
    party_spans = party_paragraph.css('span.parties_party')
    for party_span in party_spans:
        name_span = party_span.css_first('a.parties_partyname, span.parties_partyname')
        type_span = party_span.css_first('span.parties_type')

        if not name_span or not type_span:
            continue

        name = clean_string(name_span.text())
        if name.lower() == 'and':
            continue  # Skip 'AND' entries

        party_id, href = get_party_info(name_span) if name_span.tag == 'a' else ("", "")
        party_type = clean_string(type_span.text())

        party_list.append({
            "name": name,
            "type": party_type,
            "id": party_id,
            "href": href,
        })
    return party_list

# add this attribute to allow it to be added to request objects
setattr(parties, "target", ["Case"])
setattr(parties, "_default_value", [])