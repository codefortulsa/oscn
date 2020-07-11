from bs4 import BeautifulSoup

from ._helpers import table2dict

def make_property_finder(table_class, key):

    def find_property(oscn_html):
        soup = BeautifulSoup(oscn_html, "html.parser")
        table = soup.find("table", table_class)
        property_dict = table2dict(table)
        return property_dict[key]

    return find_property


find_name = make_property_finder(
    "partytable partymain", "Requested Party")
find_name.__name__ = "name"
setattr(find_name, "target", ["Party"])
setattr(find_name, "_default_value", "")


find_alias = make_property_finder(
    "partytable partymain", "Alias or Alternate Names")
find_alias.__name__ = "alias"
setattr(find_alias, "target", ["Party"])
setattr(find_alias, "_default_value", "")


find_birthmonth = make_property_finder(
    "partytable personal", "Birth Month and Year")
find_birthmonth.__name__ = "birth_month"
setattr(find_birthmonth, "target", ["Party"])
setattr(find_birthmonth, "_default_value", "")



