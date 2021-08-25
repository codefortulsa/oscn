import oscn


def test_live_request_properties():
    case1 = oscn.request.Case(county="adair", type="CM", year="2019", number=6)
    assert case1.oscn_number == "CM-2019-6"
    assert case1.index == "adair-CM-2019-6"
    assert case1.path == "/adair/CM/2019"
    assert case1.s3_key == "adair/CM/2019/6.zip"
    assert case1.file_name == "/adair/CM/2019/6.zip"


def test_init_number():
    case1 = oscn.request.Case(county="adair", type="CM", year="2019", number=6)
    assert type(case1.number) == int
    assert case1.number == 6
    case2 = oscn.request.Case(county="adair", type="CM", year="2019", number="6")
    assert type(case2.number) == str
    assert case2.number == "6"
    case3 = oscn.request.Case("adair-CM-2019-6")
    assert type(case3.number) == str
    assert case3.number == "6"
    case5 = oscn.request.Case("oklahoma-cmid-2018-00001")
    assert type(case5.number) == str
    assert case5.number == "1"
    case5 = oscn.request.Case("oklahoma-cmid-2018-008001")
    assert type(case5.number) == str
    assert case5.number == "8001"
    case5 = oscn.request.Case("oklahoma-cmid-2018-00810")
    assert type(case5.number) == str
    assert case5.number == "810"
    case5 = oscn.request.Case("oklahoma-cmid-2018-000880100")
    assert type(case5.number) == str
    assert case5.number == "880100"


def test_live_request_params_index():
    case1 = oscn.request.Case(county="adair", type="CM", year="2019", number=6)
    case2 = oscn.request.Case("adair-CM-2019-6")
    assert case2.text == case1.text
    assert case2.county == case1.county
    assert case2.type == case1.type
    assert case2.year == case1.year


def test_live_request_appellate():
    case1 = oscn.request.Case("appellate-116264")
    assert case1.number == "116264"
    assert case1.county == "appellate"

    case2 = oscn.request.Case(county="appellate", number=116264)
    assert case2.county == "appellate"
    assert case2.source == case1.source
    assert case2.style == case1.style

    case3 = oscn.request.Case(county="appellate", type="F", year="2021", number=229)
    assert case3.valid == True


def test_live_request_cmid():
    case1 = oscn.request.Case("carter-cmid-2019-639922")
    assert case1.county == "carter"
    assert case1.type == "cmid"

    case2 = oscn.request.Case(county="carter", type="cmid", number=639922)
    assert case2.county == "carter"
    assert case2.type == "cmid"
    assert case2.style == case1.style
