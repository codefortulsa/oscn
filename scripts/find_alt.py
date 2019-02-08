import oscn

# Create a test function
count_text = 'IN THE ALTERNATIVE'
def count_test(counts):
    for count in counts:
        print(count)
        if count_text in count['description']:
            return True
    return False

# define the Case attr to test and the function to use

cases = oscn.request.CaseList(county='tulsa', year='2018', stop=150)
# .find(counts=count_test)

c = next(cases)

import ipdb; ipdb.set_trace()
print(c.case_index)
print(c.counts)
