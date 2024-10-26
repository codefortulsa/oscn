import oscn
import time

from oscn import settings
from oscn.parse.lax_parties import parties
from oscn.parse.parties import bs4_parties

def test_lax_versus_bs4():
    cases = oscn.request.CaseList(
        types=["CJ","CM"],
        counties=["tulsa", "oklahoma","cleveland","texas","bexar"],
        years=["2024","2018"],
        start=4,
        stop=5,
    )


    for case in cases:
        bs4_result = bs4_parties(case.text)
        lax_result = parties(case.text)
        print("." * 100)
        print(f"Case: {case.source}")
        # print(f"BS4: {bs4_result}")
        print(f"LAX: {lax_result}")
        # print(f"cas: {case.parties}")
        assert case.parties == lax_result
        # assert bs4_result == lax_result

