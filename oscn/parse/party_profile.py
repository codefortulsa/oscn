from bs4 import BeautifulSoup

from ._helpers import table2dict


def profile(oscn_html):
    soup = BeautifulSoup(oscn_html, "html.parser")

    profile_table = soup.find("table", "partytable personal")

    profile_dict = table2dict(profile_table)

    return profile_dict


setattr(profile, "target", ["Party"])
setattr(profile, "_default_value", {})
