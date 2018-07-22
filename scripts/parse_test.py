import oscn

fp = open("examples/number_not_used.html")

find = oscn.parse.judge(fp.read())

print(find)

x = oscn.request.Case(type='CF', county='cimarron', year='2017', number=122)

cases = oscn.request.CaseList(type='CF', county='cimarron', year='2018')

for case in cases:
    print(f'case: {case.number} found: {case.judge}')
