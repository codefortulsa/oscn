import oscn

# CM-2018-299

# parties = case.parties

# carter-CM-2019-14 has cmid references


cases = oscn.request.CaseList(  types=types, counties=['carter'],
                                years=['2019'], start=13, stop=16)

print(f'---')

for case in cases:
    print(f'case: {case.index}')
    case.save(directory='data')

print(f'---')

cases = oscn.request.CaseList(  types=types, counties=['carter'],
                                years=['2019'], start=13, stop=16,
                                directory='data')


for case in cases:
    print(f'case: {case.index}')
    case.save(bucket='oscn-test-data')

print(f'---')

cases = oscn.request.CaseList(  types=types, counties=['carter'],
                                years=['2019'], start=13, stop=16,
                                bucket='oscn-test-data')

for case in cases:
    print(f'case: {case.index}')
