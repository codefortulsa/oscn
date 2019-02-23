import oscn

# CM-2018-299

# parties = case.parties

# carter-CM-2019-14 has cmid references

years = ['2019','2018']
counties = ['carter','adair']
# counties = ['tulsa']
types = ['CM','CF']


cases = oscn.request.CaseList(  types=types, county=counties,
                                year=years, start=13, stop=16)
for case in cases:
    # case.save(bucket='oscn-test-data')
    case.save(directory='data')
    print(f'case: {case.index}')


cases = oscn.request.CaseList(  types=types, county=counties,
                                year=years, start=13, stop=16,
                                directory='data')
                                # bucket='oscn-test-data')

print(f'---')

for case in cases:
    print(f'case: {case.index}')
