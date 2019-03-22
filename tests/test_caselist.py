import oscn

# carter-CM-2019-14 has three cmid references

def test_string_params():
    list1 = oscn.request.CaseList(  types='CM', counties='carter',
                                years='2019', start=13, stop=16)
    assert list1


def test_list_params():
    list1 = oscn.request.CaseList(  types=['CM','CF'], counties=['carter','tulsa'],
                                years=['2018', '2019'], start=13, stop=16)
    assert list1

def test_retrieve_cmids():
    # saving a list of cases should be retrievable by the same indexes
    list1 = oscn.request.CaseList(  types='CM', counties='carter',
                                years='2019', start=13, stop=16)

    list1_indexes = []
    for case in list1:
        # import ipdb; ipdb.set_trace()
        list1_indexes.append(case.index)
        case.save(directory='data')

    assert len(list1_indexes) == 7


    list2_indexes = []
    for idx in list1_indexes:
        filed_case = oscn.request.Case(idx,directory='data')
        assert filed_case.valid
        filed_case.save(bucket='oscn-test-data')
        list2_indexes.append(filed_case.index)

    for idx in list2_indexes:
        bucket_case = oscn.request.Case(idx, bucket='oscn-test-data')
        assert bucket_case.valid
