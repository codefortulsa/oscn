import oscn

case = oscn.request.Case(county='washington', year='2018', number=6)

print(f'judge: {case.judge}')

cases = oscn.request.CaseList(county='cimarron', year='2015')

for case in cases:
    print(f'case: {case.case_number}')
