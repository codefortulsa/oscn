import urllib.parse
from selectolax.parser import HTMLParser
from ._helpers import clean_string, MetaList


def get_party_id(link):
    try:
        href = link.attributes.get("href", "")
        if not href:
            return ""
        url = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(url.query)
        party_id = params.get("id", [""])[0]
        return party_id
    except (KeyError, IndexError, AttributeError):
        return ""


def parties(oscn_html):
    if not oscn_html:
        return []

    party_list = MetaList()
    names = []
    types = []
    party_ids = []

    try:
        parser = HTMLParser(oscn_html)
        start = parser.css_first("h2.section.party")
        if not start:
            return party_list

        # Find the next p element after the h2
        party_p = None
        current = start.next
        while current and current.tag != "p":
            current = current.next
        party_p = current

        if not party_p:
            return party_list

        party_list.text = party_p.text().strip()
        party_links = party_p.css("a")
    except Exception:
        return []

    if party_links:
        # This case has links - extract from link structure
        for link in party_links:
            name = link.text().strip()
            if not name or name.lower() == "and":
                continue

            party_id = get_party_id(link)

            # Find the parent span and then look for the type span within it
            parent_span = link.parent
            if (
                parent_span
                and parent_span.tag == "span"
                and "parties_party" in parent_span.attributes.get("class", "")
            ):
                type_span = parent_span.css_first("span.parties_type")
                party_type = type_span.text().strip() if type_span else ""
            else:
                party_type = ""

            names.append(name)
            types.append(party_type)
            party_ids.append(party_id)

    else:
        # This case uses span structure - parse each parties_party span
        party_spans = party_p.css("span.parties_party")

        for party_span in party_spans:
            name_span = party_span.css_first("span.parties_partyname")
            type_span = party_span.css_first("span.parties_type")

            if name_span:
                name = clean_string(name_span.text())
                if not name or name.lower() == "and":
                    continue

                party_type = clean_string(type_span.text()) if type_span else ""

                names.append(name)
                types.append(party_type)
                party_ids.append("")

    def Party(name, type_string, id_param):
        try:
            return {
                "name": clean_string(name) if name else "",
                "type": clean_string(type_string) if type_string else "",
                "id": id_param if id_param else "",
            }
        except Exception:
            return {"name": "", "type": "", "id": ""}

    try:
        raw_parties = map(Party, names, types, party_ids)
        for party in raw_parties:
            if party and party.get("name"):
                party_list.append(party)
    except Exception:
        pass  # Return empty list if processing fails

    return party_list

# add this attribute to allow it to be added to request objects
setattr(parties, "target", ["Case"])
setattr(parties, "_default_value", [])