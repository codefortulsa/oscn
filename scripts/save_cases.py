import oscn

# CM-2018-299

counties=['delaware','tulsa','oklahoma']
types=['CF','CM']

cases = oscn.request.CaseList(counties=counties, year='2018', types=types,stop=5)

for c in cases:
    print(c.index)
    c.save(directory='data')


cases = oscn.request.CaseList(counties=counties, year='2018', type='CF',
                                directory='data')
for case in cases:
    # import ipdb; ipdb.set_trace()
    print(case.index)
