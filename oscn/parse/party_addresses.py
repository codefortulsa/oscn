from bs4 import BeautifulSoup

from ._helpers import clean_string


def addresses(oscn_html):
    address_list = []
    get_text = lambda el: clean_string(el.text)

    soup = BeautifulSoup(oscn_html, "html.parser")

    table = soup.find("table", "partytable addresses")
    header = table.thead.find_all('th')
    keys = list(map(get_text, header))

    for row in table.tbody.find_all('tr'):
        data = row.find_all('td')
        values = map(get_text, data)
        new_dict = {k: v for k, v in zip(keys, values)}
        address_list.append(new_dict)

    return address_list


setattr(addresses, "target", ["Party"])
setattr(addresses, "_default_value", [])
