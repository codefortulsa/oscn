import oscn

# CM-2018-299
counties=['delaware','tulsa','adair']


# Create a test function
count_text = 'CHILD ENDANGERMENT'
def count_test(counts):
    for count in counts:
        if count_text in count['description']:
            return True
    return False

cases = oscn.request.CaseList(
            counties=counties, year='2018',
            type='CF',directory='data').find(
                text=count_text)

for c in cases:
    print('------------------------------------')
    print(c.source)
    print(c.counts)
    print('------------------------------------')
