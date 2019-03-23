import oscn

def test_live_request_default():
    case = oscn.request.Case()
    assert case.number == 1
    assert case.county == 'tulsa'
    assert case.type =='CF'
    assert case.year == '2019'

    cty, typ, yr, nm = case.index.split('-')
    assert case.county == cty
    assert case.type == typ
    assert case.year == yr
    assert case.number == int(nm)



def test_live_request_properties():
    case1 = oscn.request.Case(county='adair', type='CM',year='2019', number=6)
    assert case1.oscn_number == 'CM-2019-6'
    assert case1.index == 'adair-CM-2019-6'
    assert case1.path == '/adair/CM/2019'
    assert case1.s3_key == 'adair/CM/2019/6.case'
    assert case1.file_name == '/adair/CM/2019/6.case'

def test_init_number():
    case1 = oscn.request.Case(county='adair', type='CM',year='2019', number=6)
    assert type(case1.number) == int
    assert case1.number == 6
    case2 = oscn.request.Case(county='adair', type='CM',year='2019', number='6')
    assert type(case2.number) == int
    assert case2.number == 6
    case3 = oscn.request.Case('adair-CM-2019-6')
    assert type(case3.number) == int
    assert case3.number == 6
    case5 = oscn.request.Case('oklahoma-cmid-2018-00001')
    assert type(case5.number) == int
    assert case5.number == 1


def test_live_request_params_index():
    case1 = oscn.request.Case(county='adair', type='CM',year='2019', number=6)
    case2 = oscn.request.Case('adair-CM-2019-6')
    assert case2.text == case1.text
    assert case2.county == case1.county
    assert case2.type == case1.type
    assert case2.year == case1.year
    assert case2.number == case1.number


def test_live_request_appellate():
    case1 = oscn.request.Case('appellate-116264')
    assert case1.number == 116264
    assert case1.county == 'appellate'
    assert case1.type == 'IN'
    assert type(case1.number) == int
    assert case1.number == 116264

    case2 = oscn.request.Case(county='appellate', number=116264)
    assert case2.number == 116264
    assert case2.county == 'appellate'
    assert case2.type == 'IN'
    assert case2.number == 116264
    assert type(case2.number) == int
    assert case2.source == case1.source


def test_live_request_cmid():
    case1 = oscn.request.Case('carter-cmid-2019-639922')
    assert case1.number == 639922
    assert case1.county == 'carter'
    assert case1.type == 'cmid'
    assert type(case1.number) == int
    assert case1.number == 639922

    case2 = oscn.request.Case(county='carter', type='cmid', number=639922)
    assert case1.number == 639922
    assert case1.county == 'carter'
    assert case1.type == 'cmid'
    assert type(case1.number) == int
    assert case1.number == 639922
