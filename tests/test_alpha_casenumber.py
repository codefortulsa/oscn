import oscn


def dont_test_request_withalpha():
    case_params = {"number": "181A", "county": "pittsburg", "year": "2003"}

    case = oscn.request.Case(**case_params)

    assert case.valid
    assert case.county == "pittsburg"
    assert case.type == "F"
    assert case.year == "2003"
