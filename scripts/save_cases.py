import oscn


def save_cases(cases):
    for case in cases:
        print(case.index)
        case.save(directory="data")


cases = oscn.request.CaseList(counties="bryan", years="2018", types="CF", stop=60)

save_cases(cases)

cases = oscn.request.CaseList(
    types="CM", counties="carter", years="2019", start=13, stop=16
)

save_cases(cases)
