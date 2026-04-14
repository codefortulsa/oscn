import urllib.parse as urlparse

from selectolax.parser import HTMLParser


def cases(oscn_html):
    case_list = []
    tree = HTMLParser(oscn_html)

    for case_table in tree.css("table.clspg"):
        link = case_table.css_first("a")
        if not link:
            continue
        href = link.attributes.get("href", "")
        parsed = urlparse.urlparse(href)
        params = urlparse.parse_qs(parsed.query)
        if "db" not in params:
            continue
        db = params["db"][0]
        cn = link.text().strip()
        case_index = f"{db}-{cn}"
        case_list.append(case_index)

    return case_list


setattr(cases, "target", ["Docket"])
setattr(cases, "_default_value", [])


def tables(oscn_html):
    case_list = []
    tree = HTMLParser(oscn_html)

    for case_table in tree.css("table.clspg"):
        case_list.append(case_table.text(separator=" "))

    return case_list


setattr(tables, "target", ["Docket"])
setattr(tables, "_default_value", [])
