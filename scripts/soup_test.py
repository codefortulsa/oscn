import re
from bs4 import BeautifulSoup

fp = open("examples/multi_count.html")
soup = BeautifulSoup(fp, 'html.parser')
count_list = []

count_start = soup.find('h2', 'section counts')
next_sibling = count_start.find_next_sibling('p')
while next_sibling.name != 'h2':
    if next_sibling.name == 'p':
        codetags = next_sibling.find_all('strong')
        for codetag in codetags:
            codetag.extract()
        count_list.append({'description': next_sibling.text.strip()})
    next_sibling = next_sibling.next_sibling