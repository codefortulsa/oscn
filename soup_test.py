import re
from bs4 import BeautifulSoup

fp = open("examples/no_counts.html")
soup = BeautifulSoup(fp, 'html.parser')


import ipdb; ipdb.set_trace()

count_start = soup.find('h2', 'section counts')
next_sibling = count_start.find_next_sibling('p')
while next_sibling.name != 'h2':
    if next_sibling.name == 'p':
        next_sibling.strong.extract()
        count_list.append({'description': next_sibling.text.strip()})
    next_sibling = next_sibling.next_sibling
