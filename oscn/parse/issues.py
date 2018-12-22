import re

from bs4 import BeautifulSoup

from ._helpers import find_values

def issues(oscn_html):
    issue_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section issues')
    issue_table = None
    issue_table = start.find_next_sibling('table')
    key_names = ['Filed Date', 'Filed By', 'Issue']
    contains_issue = issue_table.find(string=re.compile(f'{key_names[0]}:'))
    if issue_table and contains_issue:
        # test table for issue details
        rows = issue_table.find_all('tr')
        for row in rows:
            # find the issue details
            issue_dict = find_values(row, key_names)
            # look for disposition
            issue_table =start.find_next_sibling('table')
            disp_table = (
                issue_table
                .find_next('th', 'dispositionInformation')
                .find_parent('table')
            )
            if disp_table:
                dispositions = []
                disp_keys = ['Defendant', 'Respondent', 'Disposed']
                for row in disp_table.tbody.find_all('tr'):
                    # remove formatting elements from td
                    for td in row.find_all('td'):
                        td.string = (' '.join(td.strings))
                    disp_dict = find_values(row, disp_keys)
                    dispositions.append(disp_dict)

                # add disposition to the issue dict
                issue_dict['dispositions'] = dispositions
            issue_list.append(issue_dict)

    return issue_list


# add this attribute to allow it to be added to request objects
setattr(issues, 'target', ['Case'])
setattr(issues, '_default_value', [])
