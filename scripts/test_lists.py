import oscn

# CM-2018-299

case = oscn.request.Case(county='oklahoma', year='2018', type='CM', number=299)

counts = case.counts


import ipdb; ipdb.set_trace()

# parties = case.parties

years = ['2017','2018']
counties = ['delaware','adair','love']
types = ['CF','CM']


cases = oscn.request.CaseList(types=types, county=counties, year=years, start=250, stop=300)
for case in cases:
    counts = oscn.parse.counts(case.text)
    print(f'case: {case.source}')
    print(counts)
