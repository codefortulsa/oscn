from selectolax.parser import HTMLParser

from ._helpers import clean_string

def body(oscn_html):
    tree = HTMLParser(oscn_html)
    if not (body := tree.body):
        return ""
    
    excluded_tags = {"script", "style", "div"}
    body_tags = []
    for node in body.traverse():
        if node.tag not in excluded_tags:
            body_tags.append(node.text(separator=" "))
    
    body_text = " ".join(body_tags)
    return clean_string(body_text)

setattr(body, "target", ["Case"])
setattr(body, "_default_value", "")
