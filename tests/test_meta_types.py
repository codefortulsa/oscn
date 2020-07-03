import oscn


def test_get_type_desc():
    cm_desc = oscn.type("CM")
    assert isinstance(cm_desc, str)
    assert 'CRIMINAL MISDEMEANOR' in cm_desc


def test_get_all_types():
    dict_of_all = oscn.types()
    assert isinstance(dict_of_all, dict)
