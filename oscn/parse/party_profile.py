from selectolax.parser import HTMLParser

from ._helpers import clean_string


def profile(oscn_html):
    tree = HTMLParser(oscn_html)

    table = tree.css_first("table.partytable.personal")
    if not table:
        return {}

    thead = table.css_first("thead")
    tbody = table.css_first("tbody")
    if not thead or not tbody:
        return {}

    keys = [th.text().strip() for th in thead.css("th")]
    first_row = tbody.css_first("tr")
    if not first_row:
        return {}

    values = [clean_string(td.text()) for td in first_row.css("td")]
    return dict(zip(keys, values))


setattr(profile, "target", ["Party"])
setattr(profile, "_default_value", {})
