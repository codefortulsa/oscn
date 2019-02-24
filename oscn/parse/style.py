from bs4 import BeautifulSoup

from ._helpers import clean_string

def style(oscn_html):
    soup = BeautifulSoup(oscn_html, 'html.parser')
    style_table = soup.find('table', 'caseStyle')
    style_cell = style_table.find('td')
    return clean_string(style_cell.text)

setattr(style, 'target', ['Case'])
setattr(style, '_default_value', "")
