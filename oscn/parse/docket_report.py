import urllib.parse as urlparse

from bs4 import BeautifulSoup


def cases(oscn_html):
    case_list = []
    soup = BeautifulSoup(oscn_html, "html.parser")
    case_tables = soup.findAll("table", "clspg")

    for case in case_tables:
        case_link = case.find("a")
        parsed = urlparse.urlparse(case_link["href"])
        db = urlparse.parse_qs(parsed.query)["db"][0]
        cn = case_link.text
        case_index = f"{db}-{cn}"
        case_list.append(case_index)

    return case_list


setattr(cases, "target", ["Docket"])
setattr(cases, "_default_value", [])


def tables(oscn_html):
    case_list = []
    soup = BeautifulSoup(oscn_html, "html.parser")
    case_tables = soup.findAll("table", "clspg")

    for case in case_tables:
        case_list.append(case.get_text)

    return case_list


setattr(tables, "target", ["Docket"])
setattr(tables, "_default_value", [])
