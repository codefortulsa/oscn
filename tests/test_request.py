import oscn

def test_live_request_default():
    case = oscn.request.Case()
    assert case.number == 1
    assert case.county == 'tulsa'
    assert case.type =='CF'
    assert case.year == '2019'


def test_live_request_properties():
    case1 = oscn.request.Case(county='adair', type='CM',year='2019', number=6)
    assert case1.oscn_number == 'CM-2019-6'
    assert case1.index == 'adair-CM-2019-6' 
    assert case1.path == '/adair/CM/2019'
    assert case1.s3_key == 'adair/CM/2019/6.case'
    assert case1.file_name == '/adair/CM/2019/6.case'

def test_live_request_params_index():
    case1 = oscn.request.Case(county='adair', type='CM',year='2019', number=6)
    case2 = oscn.request.Case('adair-CM-2019-6')
    assert case1.text == case2.text
    assert case2.number == '6'

def test_live_request_appellate():
    case = oscn.request.Case('appellate-116264')
    assert case.number == '116264'
