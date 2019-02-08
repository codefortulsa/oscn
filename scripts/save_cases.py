import oscn

# CM-2018-299

counties=['delaware','tulsa']

cases = oscn.request.CaseList(counties=counties, year='2018', type='CF',stop=50)

for c in cases:
    print(c.case_index)
    c.save('data')
