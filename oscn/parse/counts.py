import re
from bs4 import BeautifulSoup

from ._helpers import find_values, lists2dict

# count_re = r'Count as Filed:[^A-Z]*([A-Z|\d]*),\s(.*)'
# count_details = re.compile(count_re, re.M)



def counts(oscn_html):
    count_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    counts = soup.find_all('div', 'CountsContainer')
    if counts:
        for count in counts:
            count_keys = ['Count as Disposed', 'Count as Filed', 'Disposed', 'Date of Offense']
            count_values = find_values(count, count_keys)
            count_desc = (
                    count_values['Count as Disposed']
                    if count_values['Count as Disposed']
                    else count_values['Count as Filed']
            )

            # find violation
            found_it = False
            violated_statute=''
            for str in count.strings:
                if found_it:
                    violated_statute = str
                    break
                found_it = True if 'violation' in str.lower() else False


            save_count_info = {
                'party' : count.nobr.text,
                'offense': count_values['Date of Offense'],
                'description': count_desc,
                'disposed': count_values['Disposed'],
                'violation': violated_statute
                }
            count_list.append(save_count_info)
    else:
        count_start = soup.find('h2', 'section counts')
        next_sibling = count_start.find_next_sibling('p')
        if next_sibling:
            while next_sibling.name != 'h2':
                if next_sibling.name == 'p':
                    next_sibling.strong.extract()
                    count_list.append(
                        {'description': next_sibling.text.strip()})
                next_sibling = next_sibling.next_sibling

    return count_list

setattr(counts, 'target', ['Case'])
setattr(counts, '_default_value', [])
