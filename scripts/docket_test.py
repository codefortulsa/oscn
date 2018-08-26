import oscn

cases = oscn.request.CaseList(county='tulsa',year='2018', start=10, stop=20)

for case in cases:
    import ipdb; ipdb.set_trace()
    print(case.case_number)
    print(case.source)
    for minute in case.docket:
            print(minute)
    print('----------------------------')
