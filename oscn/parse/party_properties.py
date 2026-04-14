from selectolax.parser import HTMLParser

from ._helpers import clean_string


def _find_table_value(oscn_html, table_class, key):
    tree = HTMLParser(oscn_html)
    table = tree.css_first(f"table.{table_class}")
    if not table:
        return ""

    thead = table.css_first("thead")
    tbody = table.css_first("tbody")
    if not thead or not tbody:
        return ""

    keys = [th.text().strip() for th in thead.css("th")]
    first_row = tbody.css_first("tr")
    if not first_row:
        return ""

    values = [clean_string(td.text()) for td in first_row.css("td")]
    row_dict = dict(zip(keys, values))
    return row_dict.get(key, "")


def find_name(oscn_html):
    return _find_table_value(oscn_html, "partytable.partymain", "Requested Party")


find_name.__name__ = "name"
setattr(find_name, "target", ["Party"])
setattr(find_name, "_default_value", "")


def find_alias(oscn_html):
    return _find_table_value(oscn_html, "partytable.partymain", "Alias or Alternate Names")


find_alias.__name__ = "alias"
setattr(find_alias, "target", ["Party"])
setattr(find_alias, "_default_value", "")


def find_birthmonth(oscn_html):
    return _find_table_value(oscn_html, "partytable.personal", "Birth Month and Year")


find_birthmonth.__name__ = "birth_month"
setattr(find_birthmonth, "target", ["Party"])
setattr(find_birthmonth, "_default_value", "")
