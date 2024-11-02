import re
from selectolax.parser import HTMLParser

from ._helpers import clean_string, MetaList

issue_keys = ["Filed Date", "Filed By", "Issue"]
party_keys = ["Defendant", "Plaintiff", "Respondent", "Disposed"]


def find_values(node, key_names):
    """
    Find key word in node_text and return a dictionary of key-value pairs.
    """
    values = {}
    node_text = node.text()

    # Create a single regex pattern to match each key followed by its value
    key_pattern = "|".join(re.escape(key) for key in key_names)
    pattern = rf"({key_pattern}):\s*(.*?)(?=(?:\s*(?:{key_pattern})|$))"

    # Find all matches for key-value pairs in the text
    matches = re.finditer(pattern, node_text, re.DOTALL)

    for match in matches:
        key = match.group(1)
        value = clean_string(match.group(2).strip())
        values[key] = value

    # Ensure all keys are present in the result, even if not found in the text
    for key in key_names:
        if key not in values:
            values[key] = ""

    return values


def next_tag(node, tag):
    next_node = node.next
    while next_node:
        if next_node.tag == tag:
            return next_node
        next_node = next_node.next
    return None


def issues(oscn_html):
    issue_list = MetaList()
    tree = HTMLParser(oscn_html)
    issues_header = tree.css_first("h2.section.issues")
    if not issues_header:
        return issue_list

    issue_table = next_tag(issues_header, "table")
    docket_header = tree.css_first("h2.section.dockets")
    docket_table = next_tag(docket_header, "table")

    if (docket_table == issue_table):
        next_element = issues_header.next
        while next_element != docket_header:
            if next_element.tag == "p":
                issue_list.append(clean_string(next_element.text()))
            next_element = next_element.next
    else:
        issue_list.text = issue_table.text()
        while issue_table and "Issue #" in issue_table.text():
            issue_dict = find_values(issue_table, issue_keys)
            disp_table = next_tag(issue_table, "table")
            if disp_table != docket_table:
                issue_list.add_text(disp_table.text())
                name_details = disp_table.css("td.countpartyname")
                dispositions = disp_table.css("td.countdisposition")
                issue_dict["parties"] = []
                for name_detail, disposition in zip(name_details, dispositions):
                    name_detail_text = clean_string(name_detail.text())
                    if not name_detail_text:
                        continue
                    if ":" in name_detail_text:
                        party_type, party_name = clean_string(name_detail.text()).split(
                            ": "
                        )
                    else:
                        party_type = ""
                        party_name = name_detail_text
                    disposition_text = disposition.text()
                    disposed = (
                        disposition_text.split(": ", 1)[1]
                        if (":" in disposition_text)
                        else disposition.text()
                    )
                    party = {
                        "type": clean_string((party_type).lower()),
                        "name": clean_string(party_name),
                        "disposed": clean_string(disposed),
                    }
                    issue_dict["parties"].append(party)
                issue_list.append(issue_dict)
                issue_table = next_tag(disp_table, "table")

    return issue_list


# add this attribute to allow it to be added to request objects
setattr(issues, "target", ["Case"])
setattr(issues, "_default_value", [])
