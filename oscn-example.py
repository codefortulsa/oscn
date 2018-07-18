import oscn

case = oscn.request.Case(county='cimarron', year='2016',number=21)

print(oscn.parse.parties(case.html))

cases = oscn.request.CaseList(county='cimarron', year='2016')

for case in cases:
    name = oscn.parse.judge(case.html)
    print(f"case: {case.case_number} judge: {name}")
