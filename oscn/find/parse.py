import urllib

from bs4 import BeautifulSoup


def is_case_url(lnk):
    pass_test = False
    try:
        parent_row = lnk.find_parent("tr")
        pass_test = "resultTableRow" in parent_row.attrs["class"]
    except KeyError:
        pass
    return pass_test


def get_case_indexes(oscn_html):
    case_indexes = []
    soup = BeautifulSoup(oscn_html, "html.parser")
    counties = soup.find_all("table", "caseCourtTable")

    for county in counties:
        found_county = ""
        county_indexes = []
        links = county.find_all("a")
        case_urls = filter(is_case_url, links)
        for link in case_urls:
            oscn_query = link.attrs["href"]
            parsed_query = urllib.parse.urlparse(oscn_query)
            params = urllib.parse.parse_qs(parsed_query.query)
            found_county = params["db"][0]
            index = params["db"] + params["number"]
            case_index = "-".join(index)
            if case_index not in county_indexes:
                county_indexes.append(case_index)
        more_url = county.find("td", "moreResults")
        if more_url:
            case_indexes.append(f"{found_county}-more")
        case_indexes += county_indexes

    return case_indexes
