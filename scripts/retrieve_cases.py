import oscn

# CM-2018-299
counties=['carter','tulsa','adair']


# Create a test function
count_text = 'CHILD ENDANGERMENT'

def count_test(counts):
    for count in counts:
        if count_text in count['description']:
            return True
    return False

def log_source(source):
    print(source)
    return True

cases = oscn.request.CaseList(
            counties=counties,
            years='2019',
            types='CM',
            # bucket='oscn-cases'
            ).find(source=log_source, text=count_text)

for c in cases:
    print('------------------------------------')
    print(c.source)
    print(c.counts)
    print('------------------------------------')
