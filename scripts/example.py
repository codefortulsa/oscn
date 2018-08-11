import oscn

# single case request
case = oscn.request.Case(county='washington', year='2018', number=6)
print(f'judge: {case.judge}')
print(f'filed: {case.filed}')
print(f'parties: {case.parties}')

# all cases for a one county and year
cases = oscn.request.CaseList(county='tulsa', year='2017')


#multiple counties and multiple years
counties = ['tulsa', 'adair', 'bryan']
years = ['2016','2017']
cases = oscn.request.CaseList(county=counties, year=years, start=5, stop=7)

for case in cases:
    print(f'count: {case.county} number: {case.case_number}')



# example using find on CaseList

cases = oscn.request.CaseList(county='bryan', year='2018', stop=60)

# Create a test function
count_text = 'OBSTRUCT'
def count_test(counts):
    for count in counts:
        if count_text in count['description']:
            return True
    return False

# define the Case attr to test and the function to use
cases.find(counts=count_test)

# this will print any cases with OBSTRUCT in the counts
for case in cases:
    print(f'case: {case.case_number}')
    print(f'source: {case.source}')
