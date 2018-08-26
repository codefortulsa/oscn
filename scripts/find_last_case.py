import oscn


cases = oscn.request.CaseList(type='CF', county='delaware', year='2018', start=292)

for case in cases:
    print(case.case_number)
