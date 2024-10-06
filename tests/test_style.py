import oscn

from oscn import settings

OSCN_HEADER = settings.OSCN_REQUEST_HEADER

answer = [    
"JULIE TURLINGTON, Plaintiff, v. LESLIE FINCH, Defendant.",
"SRS DISTRIBUTION INC, Plaintiff, v. KELLY CAIN, D/B/A CAIN ROOFING, Defendant.",
"BETTY SMITH, Plaintiff, v. H AND H VENTURES LLC, D/B/A LIFEWAY HOMES, Defendant.",
"AUTO ADVANTAGE FINANCE LLC, Plaintiff, v. TATYANA KYRE BROWN, Defendant.",
"UNITED AUTO CREDIT CORPORATION, Plaintiff, v. JEREMY ANTWON WILLIAMS, Defendant, and JASMIN JANAE BYRD, Defendant.",
"TINKER FEDERAL CREDIT UNION, Plaintiff, v. SANDY KENNETH ANGEL, A/K/A KENNETH ANGEL, Defendant.",
"STATE OF OKLAHOMA EX REL Oklahoma Tax Commission, Plaintiff, v. Brian Muirhead, Defendant.",
"Amur Equipment Finance, Inc., Plaintiff, v. Traction Logistics Management, LLC and Judson Avery Cook, Defendant.",
"STATE OF OKLAHOMA EX REL Oklahoma Tax Commission, Plaintiff, v. Donaciano Gutierrez, Defendant.",
"Discover Bank, Plaintiff, v. Doug Dwayne Davis, Defendant.",
"Discover Bank, Plaintiff, v. William Gempel, Defendant.",
"Discover Bank, Plaintiff, v. Whitney Lane, Defendant.",
]

def test_style():

    cases = oscn.request.CaseList(
        types=[ "CJ"],
        counties=["tulsa", "oklahoma"],
        years=["2024"],
        start=5,
        stop=10,
    )

    results = []
    for case in cases:
        print(case.style)
        results.append(case.style)
    assert results == answer
