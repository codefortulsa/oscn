import re
from bs4 import BeautifulSoup


class Case(object):
    """docstring for Case."""
    county = ''
    case = ''
    soup = BeautifulSoup('')

    def __init__(self, county, case, html):
            self.county = county
            self.case = case
            self.soup = BeautifulSoup(html, 'html.parser')
