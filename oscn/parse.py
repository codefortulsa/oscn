import re
from bs4 import BeautifulSoup




class Case(object):
    """docstring for Case."""
    county = ''
    case = ''
    soup = BeautifulSoup('')
    count_list = []

    def __init__(self, county, case, html):
            self.county = county
            self.case = case
            self.soup = BeautifulSoup(html, 'html.parser')

    def counts(self):

        if self.count_list:
            return self.count_list

        counts = self.soup.find_all('td', 'CountDescription')

        if counts:
            for count in counts:
                import ipdb; ipdb.set_trace()
                count_details = re.compile(r'Count as Filed:[.\n\s]*([A-Z]+)\,.(.+)\,[\n\s\w\:\D]*Date of Offense\:.([\d\/]*)', re.M)
                find_desc = count_details.search(count.text)
                if find_desc.group(2):
                    self.count_list.append({'description': find_desc.group(2)})
        else:
            pass

        import ipdb; ipdb.set_trace()
        return self.count_list
