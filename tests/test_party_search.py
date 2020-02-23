import oscn


def test_init_text():
    # no text should return []
    cases = oscn.find.CaseIndexes(text='')
    cases_list = list(cases)
    assert cases_list == []



def test_find_name():
    search_params = {
        'filed_after':'12/31/2000',
        'filed_before':'01/01/2019',
        'last_name':'dungan',
    }

    cases = oscn.find.CaseIndexes(**search_params)
    cases_list = list(cases)
    assert len(cases_list) == 384

    search_params['first_name'] = 'john'
    cases = oscn.find.CaseIndexes(**search_params)
    cases_list = list(cases)
    assert len(cases_list) == 2

    # text text init
    text_cases = oscn.find.CaseIndexes(text=cases.text)
    cases_list = list(text_cases)
    assert len(cases_list) == 2


def test_find_company():
    search_params = {
        'filed_after':'12/31/2018',
        'filed_before':'01/30/2019',
        'last_name':'DISCOVER BANK',
    }

    cases = oscn.find.CaseIndexes(**search_params)
    cases_list = list(cases)
    assert len(cases_list) == 330


def test_find_district_type():
    search_params = {
        'dcct': 2,
        'apct': 42,
        'db': 'oklahoma',
        'filed_after':'02/15/2020',
        'filed_before':'02/19/2020',

    }

    cases = oscn.find.CaseIndexes(**search_params)
    cases_list = list(cases)
    assert len(cases_list) == 78
