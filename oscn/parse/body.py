from bs4 import BeautifulSoup

from ._helpers import clean_string


def body(oscn_html):
    soup = BeautifulSoup(oscn_html, "html.parser")
    body = soup.find("body")
    excluded_tags = ["script", "style", "div"]
    remove_tags = body.find_all(lambda tag: tag.name not in excluded_tags)
    body_tags = map(lambda el: el.get_text(separator=" "), remove_tags)
    body_text = " ".join(body_tags)
    return clean_string(body_text)


setattr(body, "target", ["Case"])
setattr(body, "_default_value", "")
