import oscn

from oscn.request.cases import CaseList

from oscn.parse import judge

cases = oscn.request.CaseList(county='cimarron', year='2016')

for case in cases:
    html = case['response'].text
    name = judge(html)
    case_number = case['case']
    print(f'case: {case_number} judge: {name}')
