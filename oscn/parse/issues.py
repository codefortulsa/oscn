import re

from bs4 import BeautifulSoup

from ._helpers import find_values, clean_string


issue_keys = ['Filed Date', 'Filed By', 'Issue']
party_keys = ['Defendant','Plaintiff','Respondent', 'Disposed']

def make_party_dict(**kwargs):
    # test for all keys are empty
    if all(''==v for v in kwargs.values()):
        return False

    party_type = ''
    party_name = ''

    if kwargs['Defendant']:
        party_type = 'defendant'
        party_name = kwargs['Defendant']
    elif kwargs['Plaintiff']:
        party_type = 'plaintiff'
        party_name = kwargs['Plaintiff']
    elif kwargs['Respondent']:
        party_type = 'respondent'
        party_name = kwargs['Respondent']

    return {'type':party_type, 'name': party_name, 'disposed': kwargs['Disposed']}


def issues(oscn_html):
    issue_list = []
    soup = BeautifulSoup(oscn_html, 'html.parser')
    start = soup.find('h2', 'section issues')
    issue_table = start.find_next_sibling('table')

    while re.search('Issue #', issue_table.text):
        # find the issue details
        issue_dict = find_values(issue_table, issue_keys)

        # the next table should be dispositions
        disp_table = issue_table.find_next_sibling('table')

        issue_dict['parties'] = []
        parties_rows = disp_table.find_all('tr')
        for row in parties_rows:
            # remove formatting elements from td
            for td in row.find_all('td'):
                td.string = (' '.join(td.strings))
            party_values = find_values(row, party_keys)
            party_dict = make_party_dict(**party_values)
            if party_dict:
                issue_dict['parties'].append(party_dict)

        issue_list.append(issue_dict)

        # get the next table
        issue_table = disp_table.find_next_sibling('table')

    return issue_list


# add this attribute to allow it to be added to request objects
setattr(issues, 'target', ['Case'])
setattr(issues, '_default_value', [])
