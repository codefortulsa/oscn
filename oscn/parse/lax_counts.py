import re
from selectolax.parser import HTMLParser
from ._helpers import clean_string, MetaList

def extract_text_after_keyword(keyword, stop_keywords=None):
    stop_pattern = "|".join(map(re.escape, stop_keywords)) if stop_keywords else "$"
    pattern = re.compile(rf"{re.escape(keyword)}(.*?)(?:{stop_pattern})", re.DOTALL)

    def extract(content):
        match = pattern.search(content)
        return clean_string(match.group(1)) if match else ""
    
    return extract

# Curried extract functions with pre-compiled regex patterns
extract_count_description = extract_text_after_keyword("Count as Filed:", ["in violation of"])
extract_offense_date = extract_text_after_keyword("Date of Offense:", ["<br>"])
extract_disposed_value = extract_text_after_keyword("Disposed:", ["Count as Disposed:"])

def parse_count_container(counts_container):
    count_info = {
        "party": "",
        "offense": "",
        "description": "",
        "disposed": "",
        "violation": ""
    }

    # Extract Count Description and Date of Offense
    count_description_td = counts_container.css_first("td.CountDescription")
    if not count_description_td:
        return None

    count_description_text = clean_string(count_description_td.html)
    count_info["description"] = extract_count_description(count_description_text)
    count_info["offense"] = extract_offense_date(count_description_text)

    # Extract Violation Link Text
    violation_link = count_description_td.css_first("a[href]")
    if violation_link:
        count_info["violation"] = violation_link.text(separator=" ")

    # Extract Party Name and Disposed Information
    disposition_row = counts_container.css_first("table.Disposition tbody tr")
    if disposition_row:
        party_name_td = disposition_row.css_first("td.countpartyname nobr")
        if party_name_td:
            count_info["party"] = party_name_td.text().strip()

        count_disposition_td = disposition_row.css_first("td.countdisposition")
        if count_disposition_td:
            count_disposition_text = count_disposition_td.text(separator=" ")
            count_info["disposed"] = extract_disposed_value(count_disposition_text)

    return count_info

def counts(oscn_html):
    count_list = MetaList()
    tree = HTMLParser(oscn_html)
    for counts_container in tree.css("div.CountsContainer"):
        count_info = parse_count_container(counts_container)
        if count_info:
            count_list.append(count_info)
    return count_list

setattr(counts, "target", ["Case"])
setattr(counts, "_default_value", [])
