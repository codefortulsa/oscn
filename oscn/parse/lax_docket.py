from selectolax.parser import HTMLParser
from ._helpers import clean_string, MetaList


def docket(oscn_html):
    tree = HTMLParser(oscn_html)
    docket_table = tree.css_first("table.docketlist")
    if not docket_table:
        return MetaList()

    thead = docket_table.css_first("thead")
    if not thead:
        return MetaList()
    columns = [th.text().strip().lower() for th in thead.css("th")]

    rows = docket_table.css("tbody tr")
    minutes = MetaList()
    minutes.text = docket_table.text(separator=" ")

    saved_date = ""
    for row in rows:
        cells = row.css("td")
        values = [clean_string(td.text()) if td.text().strip() else "" for td in cells]
        minute = dict(zip(columns, values))
        minute["html"] = "".join(line.strip() for line in row.html.splitlines())
        minute["date"] = minute["date"] or saved_date
        saved_date = minute["date"] or saved_date
        minutes.append(minute)

    return minutes

setattr(docket, "target", ["Case"])
setattr(docket, "_default_value", [])