from selectolax.parser import HTMLParser
from urllib.parse import parse_qs

def cmids(oscn_html):
    tree = HTMLParser(oscn_html)
    cmids = []
    links = tree.css("table.multipleRecords tbody tr a[href]")
    seen_cmids = set()
    for link in links:
        href = link.attributes.get("href", "")
        cmid_values = parse_qs(href).get("cmid", [])
        for cmid in cmid_values:
            if cmid not in seen_cmids:
                seen_cmids.add(cmid)
                cmids.append(cmid)
    
    return cmids

setattr(cmids, "target", ["Case"])
setattr(cmids, "_default_value", [])
