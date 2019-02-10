import oscn


cases = oscn.request.CaseList(type='CF', county='love', year='2017', start=300)

for case in cases:
    print(case.oscn_number)
