import oscn

# CM-2018-299

counties=['delaware','tulsa','oklahoma']
types=['CF']

# cases = oscn.request.CaseList(counties=counties, year='2018', types=types,stop=5)
#
# for c in cases:
#     # import ipdb; ipdb.set_trace()
#     print(c.index)
#     c.save(bucket='oscn-data')

#
cases = oscn.request.CaseList(counties=counties, year='2018', type='CF',
                                bucket='oscn-data')
for case in cases:
    # import ipdb; ipdb.set_trace()
    print(case.index)
