import re
from bs4 import BeautifulSoup

count_re = r'Count as Filed:[^A-Z]*([A-Z|\d]*),\s(.*)'


def counts(oscn_html):
    count_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    counts = soup.find_all('td', 'CountDescription')
    if counts:
        for count in counts:
            count_details = re.compile(count_re, re.M)
            find_desc = count_details.search(count.text)
            if find_desc.group:
                count_list.append({'description': find_desc.group(2).strip()})
    else:
        count_start = soup.find('h2', 'section counts')
        next_sibling = count_start.find_next_sibling('p')
        if next_sibling:
            while next_sibling.name != 'h2':
                if next_sibling.name == 'p':
                    next_sibling.strong.extract()
                    count_list.append({'description': next_sibling.text.strip()})
                next_sibling = next_sibling.next_sibling

    return count_list

setattr(counts,'target',['OSCNrequest'])
