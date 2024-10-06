from selectolax.parser import HTMLParser
from unicodedata import normalize

def clean_string(some_string):
    # Normalize unicode characters
    normal_str = normalize("NFKD", some_string)
    # Remove all types of whitespace by splitting and rejoining
    condensed = ' '.join(normal_str.split())
    return condensed

def style(oscn_html):
    tree = HTMLParser(oscn_html)
    if style_table := tree.css('table.caseStyle'):
        if style_cell := style_table[0].css_first('td'):
            if text := style_cell.text():
                return clean_string(text)
    return ""

setattr(style, "target", ["Case"])
setattr(style, "_default_value", "")
