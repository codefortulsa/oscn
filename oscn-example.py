import oscn

from oscn.request.cases import CaseList, Case

from oscn.parse import parties, judge

case = oscn.request.Case(county='cimarron', year='2016',number=21)

html = case.request()['response'].text

print(parties(html))

cases = oscn.request.CaseList(county='cimarron', year='2016')

for case in cases:
    html = case['response'].text
    name = oscn.parse.judge(html)
    print(f"case: {case['case'] } judge: {name}")
