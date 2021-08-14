import oscn

search_for_text = "OBSTRUCT"
known_good = ["bryan-CF-2018-4", "bryan-CF-2018-24", "bryan-CF-2018-51"]


def test_find_text_in_text():
    cases = oscn.request.CaseList(counties="bryan", years="2018", types="CF", stop=60)
    cases.find(text=search_for_text)

    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == "bryan"
        assert case.year == "2018"
        assert int(case.number) <= 60
        assert search_for_text in case.text

    assert found_index == known_good


def test_find_function():
    def count_test(counts):
        for count in counts:
            if search_for_text in count["description"]:
                return True
        return False

    cases = oscn.request.CaseList(counties="bryan", years="2018", types="CF", stop=60)
    cases.find(counts=count_test)

    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == "bryan"
        assert case.year == "2018"
        assert int(case.number) <= 60
        assert search_for_text in case.text
    assert found_index == known_good


def test_find_bucket_text():

    cases = oscn.request.CaseList(
        counties="bryan", years="2018", types="CF", stop=60, bucket="oscn-test-data"
    )

    cases.find(text=search_for_text)

    found_index = []

    for case in cases:
        found_index.append(case.index)
        assert case.county == "bryan"
        assert case.year == "2018"
        assert int(case.number) <= 60
        assert search_for_text in case.text
    assert found_index == known_good


def test_find_directory_text():

    cases = oscn.request.CaseList(
        counties="bryan", years="2018", types="CF", stop=60, directory="data"
    )

    cases.find(text=search_for_text)

    found_index = []
    for case in cases:
        found_index.append(case.index)
        assert case.county == "bryan"
        assert case.year == "2018"
        assert int(case.number) <= 60
        assert search_for_text in case.text
    assert found_index == known_good


def test_find_multi_funcs():
    source_calls = 0
    count_calls = 0
    case_count = 0

    def log_source(source):
        nonlocal source_calls
        source_calls = source_calls + 1
        return True

    def log_counts(counts):
        nonlocal count_calls
        count_calls += 1
        return True

    cases = oscn.request.CaseList(
        counties="bryan", years="2018", types="CF", stop=20, directory="data"
    )

    cases.find(source=log_source, counts=log_counts)

    for case in cases:
        case_count += 1

    # import pdb; pdb.set_trace()

    assert source_calls == case_count
    assert count_calls == case_count
    assert source_calls == count_calls
