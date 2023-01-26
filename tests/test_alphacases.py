import oscn


def test_case_with_alpha():
    case_index = "stephens-CS-2021-00267R"

    case = oscn.request.Case(case_index)

    assert case.valid
