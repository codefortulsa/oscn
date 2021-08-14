import oscn

valid_cases = [
    "appellate-118615",
    "appellate-SCBD-6889",
    "appellate-DF-118613",
    "appellate-F-2021-229",
    "appellate-118610",
    "appellate-MA-118610",
    "appellate-118609",
    "appellate-PR-118611",
    "appellate-DF-118616",
    "appellate-MA-118618",
    "appellate-DF-118620",
    "appellate-IN-118622",
    "appellate-DF-118617",
    "appellate-DF-118619",
    "appellate-DF-118623",
    "appellate-DF-118625",
    "appellate-SCBD-6893",
    "appellate-SCBD-6894",
    "appellate-HC-118629",
    "appellate-PR-118630",
    "appellate-DF-118627",
    "appellate-SD-118628",
    "appellate-DF-118635",
    "appellate-PR-118633",
    "appellate-SCBD-6895",
    "appellate-SD-118634",
    "appellate-CI-118636",
    "appellate-PR-118640",
    "appellate-PR-118646",
    "appellate-DF-118645",
    "appellate-MA-118637",
    "appellate-PR-118639",
    "appellate-IN-118641",
    "appellate-CQ-118638",
    "appellate-118642",
    "appellate-SD-118644",
    "appellate-SD-118643",
    "appellate-118648",
    "appellate-CI-118647",
    "appellate-118649",
    "appellate-SCBD-6896",
    "appellate-DF-118650",
    "appellate-DF-118654",
    "appellate-DF-118653",
    "appellate-118652",
    "appellate-DF-118651",
]


def test_appellate_types():
    for indx in valid_cases:
        print(indx)
        case = oscn.request.Case(indx)
        assert case.valid
