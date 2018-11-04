# Some case URL's return a list of 'sbu' caseStyle
# See an example in examples/multi_case_table.html
# this function looks return a list of cmids for if found

from bs4 import BeautifulSoup
from urllib.parse import parse_qs


def cmids(oscn_html):
    soup = BeautifulSoup(oscn_html, 'html.parser')
    cmids = []
    ref_table = soup.find('table', 'multipleRecords')
    if ref_table:
        for row in ref_table.find('tbody').find_all('tr'):
            href = row.find('a')['href']
            cmids += parse_qs(href)['cmid']

    return cmids

setattr(cmids, 'target', ['Case'])
