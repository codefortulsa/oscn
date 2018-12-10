import oscn

# case = oscn.request.Case(county='tulsa', year='2018', type='FD', number=1)
#
# import ipdb; ipdb.set_trace()
#
# parties = case.parties

types = ['CV', 'PB', 'FD']


cases = oscn.request.CaseList(types=types, county='tulsa', year='2017', start=700, stop=710)
for case in cases:
    issues = oscn.parse.issues(case.text)
    print(issues)
