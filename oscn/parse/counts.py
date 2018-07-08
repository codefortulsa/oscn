import re
from bs4 import BeautifulSoup


def counts(oscn_page):
    count_list = []
    soup = BeautifulSoup(oscn_page, 'html.parser')
    counts = soup.find_all('td', 'CountDescription')
    if counts:
        for count in counts:
            count_details = re.compile(r'Count as Filed:[.\n\s]*([A-Z]+)\,.(.+)\,[\n\s\w\:\D]*Date of Offense\:.([\d\/]*)', re.M)
            find_desc = count_details.search(count.text)
            if find_desc.group(2):
                count_list.append({'description': find_desc.group(2)})
    else:
        count_start = soup.find('h2', 'section counts')
        next_sibling = count_start.find_next_sibling('p')
        while next_sibling.name != 'h2':
            if next_sibling.name == 'p':
                next_sibling.strong.extract()
                count_list.append({'description': next_sibling.text.strip()})
            next_sibling = next_sibling.next_sibling

    return count_list
