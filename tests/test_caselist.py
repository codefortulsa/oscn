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
    list1 = oscn.request.CaseList(  types='CM', counties='carter',
                                years='2019', start=13, stop=16)

    # saving a list of cases should be retrievable by the same indexes
    list1 = oscn.request.CaseList(  types='CM', counties='carter',
                                years='2019', start=13, stop=16)

    list1_indexes = []
    for case in list1:
        list1_indexes.append(case.index)
        case.save(directory='data')
# should be:
# ['carter-CM-2019-13', 'carter-CM-2019-14', 'carter-cmid-639922', 'carter-cmid-639923', 'carter-cmid-645034', 'carter-CM-2019-15', 'carter-CM-2019-16']
    assert len(list1_indexes) == 7

    for idx in list1_indexes:
        oscn.request.Case(idx,directory='data')
        assert case.valid
