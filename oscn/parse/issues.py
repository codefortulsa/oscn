import re

from bs4 import BeautifulSoup

from ._helpers import lists2dict, clean_string


def issues(oscn_html):
    issue_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section issues')
    issue_table = None
    issue_table = start.find_next_sibling('table')
    if issue_table:
        rows = issue_table.find_all('tr')
        for row in rows:
            key_words = ['Filed Date', 'Filed By', 'Issue']
            values = []
            for word in key_words:
                word_element = row.find(string=re.compile(f'{word}:'))
                if word_element:
                    word_value = word_element.split(':')[1]
                else:
                    word_value = ''
                values.append(clean_string(word_value))

            issue_list.append(lists2dict(key_words, values))
    return issue_list


# add this attribute to allow it to be added to request objects
setattr(issues, 'target', ['Case'])
setattr(issues, '_default_value', [])
