import oscn

known_good = ['bryan-CF-2018-4', 'bryan-CF-2018-24', 'bryan-CF-2018-51']

def test_find_text_in_text():
    cases = oscn.request.CaseList(counties='bryan', years='2018', types='CF', stop=60)
    # define the Case attr to test and the function to use
    cases.find(text='OBSTRUCT')
    # this will print any cases with OBSTRUCT in the counts
    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == 'bryan'
        assert case.year == '2018'
        assert case.number <= 60
    assert found_index == known_good


def test_find_function():
    # Create a test function
    count_text = 'OBSTRUCT'
    def count_test(counts):
        for count in counts:
            if count_text in count['description']:
                return True
        return False

    cases = oscn.request.CaseList(counties='bryan', years='2018', types='CF', stop=60)
    # define the Case attr to test and the function to use
    cases.find(counts=count_test)

    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == 'bryan'
        assert case.year == '2018'
        assert case.number <= 60
    assert found_index == known_good
