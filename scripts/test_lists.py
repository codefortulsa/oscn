import oscn

# case = oscn.request.Case(county='tulsa', year='2018', type='FD', number=1)
#
# import ipdb; ipdb.set_trace()
#
# parties = case.parties

types = ['CM', 'CV', 'CF', 'PB', 'FD']


cases = oscn.request.CaseList(types=types, county='tulsa', year='2017', start=50, stop=55)
for case in cases:
    print(case.case_number)
    print(case.parties)
