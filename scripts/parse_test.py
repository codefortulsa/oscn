from oscn.request import Case, CaseList
import oscn.parse

fp = open("examples/number_not_used.html")

find = oscn.parse.judge(fp.read())

print(find)

x = Case(type='CF', county='cimarron', year='2017', number=122)

import ipdb; ipdb.set_trace()

cases = CaseList(type='CF', county='cimarron', year='2018')


for case in cases:
    # import ipdb; ipdb.set_trace()
    find = oscn.parse.judge(case['response'].text)
    number = case['case']
    print(f'case: {number} found: {find}')
