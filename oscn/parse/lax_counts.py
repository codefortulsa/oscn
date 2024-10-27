from selectolax.parser import HTMLParser
from ._helpers import clean_string, MetaList
import re

def counts(oscn_html):
    count_list = MetaList()
    tree = HTMLParser(oscn_html)
    if (containers := tree.css("div.CountsContainer")):
        # Extract counts information from "Counts" table
        for counts_container in containers:
            counts_container_text = clean_string(counts_container.html)
            count_table = counts_container.css("table.Counts tbody tr")
            count_description_td = count_table[0].css_first("td.CountDescription")
            if not count_description_td:
                continue
            
            # Extract text from CountDescription
            count_description_text = clean_string(count_description_td.html)
            # Extract description after "Count as Filed:" until "in violation of" or <br>
            count_desc = ""
            if "Count as Filed:" in count_description_text:
                count_desc_parts = count_description_text.split("Count as Filed:")
                if len(count_desc_parts) > 1:
                    count_desc = count_desc_parts[1].split(", in violation of")[0]
            # Use "Count as Disposed" if it exists to override description
            if "Count as Disposed:" in counts_container_text:
                count_as_disposed_parts = counts_container_text.split("Count as Disposed:")
                if len(count_as_disposed_parts) > 1:
                    count_desc = clean_string(count_as_disposed_parts[1].split('<br>')[0])

            # Extract date of offense
            offense_date = ""
            if "Date of Offense:" in count_description_text:
                offense_date_parts = count_description_text.split("Date of Offense:")
                if len(offense_date_parts) > 1:
                    offense_date = offense_date_parts[1].split('<br>')[0].strip()
                    offense_date = clean_string(offense_date)

            # Extract violation link text
            violation_link = count_description_td.css_first("a[href]")
            violated_statute = violation_link.text(separator=" ") if violation_link else ""

            # Extract party name and disposed information from the "Disposition" table
            disposition_row = counts_container.css_first("table.Disposition tbody tr")
            if disposition_row:
                party_name_td = disposition_row.css_first("td.countpartyname nobr")
                party_name = party_name_td.text().strip() if party_name_td else ""

                count_disposition_td = disposition_row.css_first("td.countdisposition")
                if count_disposition_td:
                    # Extract disposed information after "Disposed:" until <br> or end of line
                    count_disposition_text = count_disposition_td.text(separator=" ")
                    disposed_value = ""
                    if "Disposed:" in count_disposition_text:
                        disposed_parts = count_disposition_text.split("Count as Disposed:")
                        if len(disposed_parts) > 1:
                            disposed_value = clean_string(disposed_parts[0].split('Disposed:')[1])
                else:
                    disposed_value = ""
            else:
                party_name = ""
                disposed_value = ""

            save_count_info = {
                "party": party_name,
                "offense": offense_date,
                "description": count_desc,
                "disposed": disposed_value,
                "violation": violated_statute,
            }
            count_list.append(save_count_info)

    return count_list


setattr(counts, "target", ["Case"])
setattr(counts, "_default_value", [])
