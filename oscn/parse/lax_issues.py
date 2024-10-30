import re
from selectolax.parser import HTMLParser

from ._helpers import clean_string, MetaList

issue_keys = ["Filed Date", "Filed By", "Issue"]
party_keys = ["Defendant", "Plaintiff", "Respondent", "Disposed"]


def find_values(node, key_names):
    """
    Find key word in node_text and return a dictionary of key value pairs
    """
    values = {}
    node_text = node.text()
    for key in key_names:
        # Construct pattern to find the key followed by a colon and capture until the next key or end
        pattern = rf"{key}:\s*(.*?)(?=(?:\s*{key_names[0]}|\s*{key_names[1]}|\s*{key_names[2]}|$))"
        match = re.search(pattern, node_text, re.DOTALL)
        if match:
            values[key] = clean_string(match.group(1).strip())
        else:
            values[key] = ""

    return values


def make_party_dict(issue_node):

    if kwargs["Defendant"]:
        party_type = "defendant"
        party_name = kwargs["Defendant"]
    elif kwargs["Plaintiff"]:
        party_type = "plaintiff"
        party_name = kwargs["Plaintiff"]
    elif kwargs["Respondent"]:
        party_type = "respondent"
        party_name = kwargs["Respondent"]

    return {"type": party_type, "name": party_name, "disposed": kwargs["Disposed"]}


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

    is_docket = docket_table == issue_table

    if is_docket:
        next_sibling = issues_header.next
        while next_sibling != docket_header:
            if next_sibling.tag == "p":
                issue_list.append(clean_string(next_sibling.text()))
            next_sibling = next_sibling.next
    else:
        while issue_table and "Issue #" in issue_table.text():
            issue_dict = find_values(issue_table, issue_keys)
            disp_table = next_tag(issue_table, "table")
            if disp_table != docket_table:
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
