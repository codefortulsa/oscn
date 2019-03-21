import oscn

cases = oscn.request.CaseList(counties='delaware',years='2018', start=18, stop=22, types='CF')

for case in cases:
    print(case.number)
    print(case.source)
    print(f'judge: {case.judge} counts: {case.counts}')
    print('----------------------------')
