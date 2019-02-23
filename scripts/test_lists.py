import oscn

# CM-2018-299

# parties = case.parties

# carter-CM-2019-14 has cmid references

years = ['2019']
counties = ['carter']
# counties = ['tulsa']
types = ['CM']


cases = oscn.request.CaseList(  types=types, county=counties,
                                year=years, start=13, stop=16)
for case in cases:
    case.save(bucket='oscn-case-data')
    case.save(directory='data')
    print(f'case: {case.index}')


cases = oscn.request.CaseList(  types=types, county=counties,
                                year=years, start=13, stop=16,
                                directory='data')

print(f'---')

for case in cases:
    print(f'case: {case.index}')
