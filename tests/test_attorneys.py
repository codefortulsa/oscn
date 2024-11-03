import oscn
import time

from oscn import settings
from oscn.parse.lax_attorneys import attorneys
from oscn.parse.bs4_attorneys import bs4_attorneys

OSCN_HEADER = settings.OSCN_REQUEST_HEADER

def test_lax_versus_bs4():
    cases = oscn.request.CaseList(
        types=["CJ","CM"],
        counties=["tulsa", "oklahoma","mayes","wagoner","creek","okmulgee","osage",],
        years=["2024","2018"],
        start=4,
        stop=5,
    )


    for case in cases:
        bs4_result = bs4_attorneys(case.text)
        lax_result = attorneys(case.text)
        print("." * 100)
        print(f"Case: {case.source}")
        print(f"BS4: {bs4_result}")
        print(f"LAX: {lax_result}")
        print("case.attorneys: ", case.attorneys)
        assert case.attorneys == lax_result
        assert bs4_result == lax_result

