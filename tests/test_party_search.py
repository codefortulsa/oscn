import oscn


def test_find_name():
    search_params = {
        'filed_after':'12/31/2000',
        'filed_before':'01/01/2019',
        'last':'dungan',
    }

    cases = oscn.find.CaseIndexes(**search_params)
    cases_list = list(cases)
    assert len(cases_list) == 384

    search_params['first'] = 'john'
    cases = oscn.find.CaseIndexes(**search_params)
    cases_list = list(cases)
    assert len(cases_list) == 2

def test_find_company():
    search_params = {
        'filed_after':'12/31/2018',
        'filed_before':'01/30/2019',
        'last':'DISCOVER BANK',
    }

    cases = oscn.find.CaseIndexes(**search_params)
    cases_list = list(cases)
    assert len(cases_list) == 330
