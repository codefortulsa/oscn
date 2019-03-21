import oscn

def test_parse_string_response():
    case = oscn.request.Case('cleveland-CF-2016-84')
    assert case.judge == 'WALKLEY, LORI'
    assert case.filed == '01/19/2016'
    assert case.closed == '04/28/2016'
