import oscn

case = oscn.request.Case(county='tulsa', year='2017', type='FD', number=387)

i = case.issues


import ipdb; ipdb.set_trace()
#
# parties = case.parties

years = ['2017', '2018']
counties = ['tulsa', 'oklahoma']
types = ['CV', 'PB', 'FD']

import ipdb; ipdb.set_trace()

cases = oscn.request.CaseList(types=types, county='tulsa', year='2017', start=700, stop=710)
for case in cases:
    issues = oscn.parse.issues(case.text)
    print(issues)
