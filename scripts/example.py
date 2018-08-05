import oscn

# example of a single case request
case = oscn.request.Case(county='washington', year='2018', number=6)

print(f'judge: {case.judge}')
print(f'filed: {case.filed}')
print(f'parties: {case.parties}')

# example of cases for a single county and year
# this range also includes an unused case number
cases = oscn.request.CaseList(county='adair', year='2017', start=120, stop=130)

for case in cases:
    print(f'case: {case.case_number}')
    print(f'closed: {case.closed}')
    print(f'source: {case.source}')

# example of multiple counties and multiple years
counties = ['tulsa', 'adair', 'bryan']
years = ['2016','2017']
cases = oscn.request.CaseList(county=counties, year=years, start=5, stop=7)

for case in cases:
    print(f'count: {case.county} number: {case.case_number}')
