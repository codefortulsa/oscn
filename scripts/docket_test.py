import re
import oscn
# Create a test function
search_for = re.compile(r'reappear', re.I | re.M)
def test_minutes(docket):
    for min in docket:
        if search_for.search(min['description']):
            return True
    return False

# define the Case attr to test and the function to use

cases = oscn.request.CaseList(county='tulsa', year='2018', start= 1, stop=350).find(docket=test_minutes)

import ipdb; ipdb.set_trace()

next(cases)
