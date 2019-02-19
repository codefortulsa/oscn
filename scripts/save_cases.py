import oscn

# CM-2018-299

counties=['delaware','adair']
types=['CF','CM']
years=['2013','2012']


cases = oscn.request.CaseList(counties=counties, year=years, type=types,stop=3)
for case in cases:
    print(case.index)
    case.save(bucket='oscn-test-data')
    case.save(directory='data')


cases = oscn.request.CaseList(counties=counties, year=years, type=types,bucket='oscn-test-data')
for case in cases:
    print(case.parties)

cases = oscn.request.CaseList(counties=counties, year=years, type=types,directory='data')
for case in cases:
    print(case.events)
