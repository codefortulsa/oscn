import oscn

import requests

from oscn import settings

OSCN_HEADER = settings.OSCN_REQUEST_HEADER


def test_source_works():

    cases = oscn.request.CaseList(
        types=["CM", "CF", "CJ"],
        counties=["tulsa", "carter", "cimarron", "oklahoma"],
        years=["2019", "2020"],
        start=5,
        stop=10,
    )

    for case in cases:
        print(case.source)
        response = requests.get(case.source, headers=OSCN_HEADER, verify=False)
        assert response.status_code == 200
