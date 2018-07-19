import oscn

case = oscn.request.Case(county='cimarron', year='2016',number=21)

print(f'parties: {case.parties}')

cases = oscn.request.CaseList(county='cimarron', year='2016')

for case in cases:
    print(f"case: {case.case_number} judge: {case.judge}")
