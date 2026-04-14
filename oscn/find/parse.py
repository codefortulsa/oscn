import urllib.parse

from selectolax.parser import HTMLParser


def get_case_indexes(oscn_html):
    case_indexes = []
    tree = HTMLParser(oscn_html)
    counties = tree.css("table.caseCourtTable")

    for county in counties:
        found_county = ""
        county_indexes = []

        for link in county.css("tr.resultTableRow a[href]"):
            href = link.attributes.get("href", "")
            parsed_query = urllib.parse.urlparse(href)
            params = urllib.parse.parse_qs(parsed_query.query)
            if "db" not in params or "number" not in params:
                continue
            found_county = params["db"][0]
            case_index = f"{found_county}-{params['number'][0]}"
            if case_index not in county_indexes:
                county_indexes.append(case_index)

        if county.css_first("td.moreResults"):
            case_indexes.append(f"{found_county}-more")

        case_indexes += county_indexes

    return case_indexes
