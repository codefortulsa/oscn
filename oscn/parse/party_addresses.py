from selectolax.parser import HTMLParser

from ._helpers import clean_string


def addresses(oscn_html):
    address_list = []
    tree = HTMLParser(oscn_html)

    table = tree.css_first("table.partytable.addresses")
    if not table:
        return address_list

    thead = table.css_first("thead")
    tbody = table.css_first("tbody")
    if not thead or not tbody:
        return address_list

    keys = [th.text().strip() for th in thead.css("th")]

    for row in tbody.css("tr"):
        values = [clean_string(td.text()) for td in row.css("td")]
        address_list.append(dict(zip(keys, values)))

    return address_list


setattr(addresses, "target", ["Party"])
setattr(addresses, "_default_value", [])
