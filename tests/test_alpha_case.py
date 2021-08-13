import oscn


def test_request_withalpha():
    case_params = {
        "number": "181A",
        "type": "F",
        "county": "pittsburg",
        "year": "2003"
    }

    case = oscn.request.Case(**case_params)

    assert case.valid
    assert case.county == "pittsburg"
    assert case.type == "F"
    assert case.year == "2003"
