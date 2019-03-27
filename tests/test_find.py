import oscn

search_for_text='OBSTRUCT'
known_good = ['bryan-CF-2018-4', 'bryan-CF-2018-24', 'bryan-CF-2018-51']

def test_find_text_in_text():
    cases = oscn.request.CaseList(  counties='bryan',years='2018',
                                    types='CF', stop=60)
    cases.find(text=search_for_text)
    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == 'bryan'
        assert case.year == '2018'
        assert case.number <= 60
        assert search_for_text in case.text
    assert found_index == known_good


def test_find_function():

    def count_test(counts):
        for count in counts:
            if search_for_text in count['description']:
                return True
        return False

    cases = oscn.request.CaseList(counties='bryan', years='2018', types='CF', stop=60)
    cases.find(counts=count_test)

    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == 'bryan'
        assert case.year == '2018'
        assert case.number <= 60
        assert search_for_text in case.text
    assert found_index == known_good

def test_find_bucket_text():

    cases = oscn.request.CaseList(  counties='bryan', years='2018', types='CF',
                                    stop=60,bucket='oscn-cases')

    cases.find(text=search_for_text)

    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == 'bryan'
        assert case.year == '2018'
        assert case.number <= 60
        assert search_for_text in case.text
    assert found_index == known_good

def test_find_directory_text():

    cases = oscn.request.CaseList(  counties='bryan', years='2018', types='CF',
                                    stop=60, directory='data')

    cases.find(text=search_for_text)

    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == 'bryan'
        assert case.year == '2018'
        assert case.number <= 60
        assert search_for_text in case.text
    assert found_index == known_good
