import oscn


def test_two_issue_formats():
    case1 = oscn.request.Case("choctaw-SC-2020-118")
    assert case1.issues[0] == "1. EVICTION SMALL CLAIMS(UNDER $5000.00)"

    case2 = oscn.request.Case("tulsa-SC-2020-118")
    assert case2.issues[0]["Issue"] == "FORCIBLE ENTRY & DETAINER <$5000.00. (SCFED1)"
