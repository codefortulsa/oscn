import oscn

# # single case request
case = oscn.request.Case(county="mayes", year="2018", number=11)
print(f"judge: {case.judge}")
print(f"filed: {case.filed}")
print(f"parties: {case.parties}")

for min in case.docket:
    print(min)

# # all cases for a one county and year
cases = oscn.request.CaseList(county="tulsa", year="2017")
#
#
# # multiple types, multiple counties, or multiple years
types = ["CM", "CF"]
counties = ["tulsa", "adair", "bryan"]
years = ["2016", "2017"]
cases = oscn.request.CaseList(county=counties, year=years, start=5, stop=7)


for case in cases:
    print(f"county: {case.county} number: {case.oscn_number}")


# example using find on CaseList

cases = oscn.request.CaseList(county="bryan", year="2018", stop=60)

# Create a test function
count_text = "OBSTRUCT"


def count_test(counts):
    for count in counts:
        if count_text in count["description"]:
            return True
    return False


# define the Case attr to test and the function to use
cases.find(counts=count_test)

# this will print any cases with OBSTRUCT in the counts
for case in cases:
    print(f"case: {case.oscn_number}")
    print(f"source: {case.source}")
