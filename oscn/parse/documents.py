import re
from selectolax.parser import HTMLParser
from urllib.parse import urlparse, parse_qs
import logging
from dataclasses import dataclass
from ._helpers import clean_string, MetaList
from oscn.settings import OSCN_DOCKETS_URL

logger = logging.getLogger(__name__)

ID_REGEX = re.compile(r"\(#(\d+)\)")
TITLE_END_REGEX = re.compile(r"\s+Document\s+(?:Available|Unavailable)")


def documents(oscn_html):
    tree = HTMLParser(oscn_html)
    docket_table = tree.css_first("table.docketlist")
    if not docket_table:
        return MetaList()

    docs = MetaList()
    docs.text = docket_table.text(separator=" ")

    # Use the table header to create a dynamic mapping of columns.
    # This is more robust than relying on fixed column indexes.
    try:
        columns = [
            th.text().strip().lower()
            for th in docket_table.css_first("thead").css("th")
        ]
    except AttributeError:
        # Handle cases where the table might be malformed or lack a header.
        return MetaList()

    saved_date = ""
    for row in docket_table.css("tbody tr"):
        cells = row.css("td")
        # Create a dictionary for the current row's data.
        row_data = {col: clean_string(cell.text()) for col, cell in zip(columns, cells)}

        # Persist the date across rows that don't have one explicitly.
        current_date = row_data.get("date") or saved_date
        saved_date = current_date
        row_data["date"] = current_date

        description_cell = row.css_first("td:nth-child(3)")
        if not description_cell:
            continue

        links = description_cell.css("a")
        for link in links:
            if link.text(strip=True) == "PDF":
                href = link.attributes.get("href")
                if href:
                    description_text = description_cell.text()
                    id_match = ID_REGEX.search(description_text)
                    doc_id = int(id_match.group(1)) if id_match else None

                    title_end_match = TITLE_END_REGEX.search(description_text)
                    if title_end_match:
                        title_text = description_text[: title_end_match.start()]
                    else:
                        # If the standard text is missing, fall back to the full description.
                        title_text = description_text

                    doc = {
                        "id": doc_id,
                        "title": clean_string(title_text),
                        "url": f"{OSCN_DOCKETS_URL}/{href}",
                        "date": row_data.get("date", ""),
                        "code": row_data.get("code", ""),
                        "party": row_data.get("party", ""),
                    }
                    docs.append(doc)

    return docs


setattr(documents, "target", ["Case"])
setattr(documents, "_default_value", [])
