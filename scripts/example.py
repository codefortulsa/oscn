import oscn

case = oscn.request.Case(county='washington', year='2018', number=6)

print(f'judge: {case.judge}')
print(f'filed: {case.filed}')
print(f'parties: {case.parties}')

cases = oscn.request.CaseList(county='tulsa', year='2015', start=5, stop=10)

for case in cases:
    print(f'case: {case.case_number}')
    print(f'closed: {case.closed}')
    print(f'source: {case.source}')
