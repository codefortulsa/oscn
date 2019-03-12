import oscn


cases = ['tulsa-CF-2018-01048',
'tulsa-CJ-2016-3196',
'tulsa-CJ-2018-4616',
'tulsa-CV-2019-0012',
'mayes-CJ-2018-0104']

for case_index in cases:
    case = oscn.request.Case(case_index)
    print(case.events)
    print(case.source)
    print('---')
