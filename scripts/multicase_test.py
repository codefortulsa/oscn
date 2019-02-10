import oscn

cases = oscn.request.CaseList(county='delaware',year='2018', start=18, stop=22, type='CF')

for case in cases:
    print(case.oscn_number)
    print(case.source)
    print(f'judge: {case.judge} counts: {case.counts}')
    print('----------------------------')
