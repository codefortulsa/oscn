from selectolax.parser import HTMLParser
from ._helpers import clean_string, MetaList

def attorneys(oscn_html):
    attorney_list = MetaList()
    tree = HTMLParser(oscn_html)

    attorneys_h2 = tree.css_first('h2.section.attorneys')
    if not attorneys_h2:
        return attorney_list

    # Loop through elements until a table is found or another h2 is found
    next_element = attorneys_h2.next
    while next_element:
        if next_element.tag == 'table':
            attorney_table = next_element
            attorney_list.text = attorney_table.text(strip=True)
            break
        if next_element.tag == 'h2':
            return attorney_list
        next_element = next_element.next
    else:
        return attorney_list

    # Extract text from the attorney table
    rows = attorney_table.css('tr')  # Use 'tr' directly to avoid dependency on 'tbody'
    for row in rows:
        row_tds = row.css('td')
        if len(row_tds) < 2:
            continue

        # Extract name and address properly by splitting lines and cleaning each part
        attorney_with_address = [clean_string(line) for line in row_tds[0].text(separator="\n").split('\n') if line.strip()]
        if not attorney_with_address:
            continue

        name = attorney_with_address[0]
        address = attorney_with_address[1:]
        representing = clean_string(row_tds[1].text())

        attorney_list.append(
            {
                "name": name,
                "address": address,
                "representing": representing,
            }
        )
    return attorney_list

# add this attribute to allow it to be added to request objects
setattr(attorneys, "target", ["Case"])
setattr(attorneys, "_default_value", [])