import oscn

def test_parse_string_response():
    case = oscn.request.Case('cleveland-CF-2016-84')
    assert case.judge == 'WALKLEY, LORI'
    assert case.filed == '01/19/2016'
    assert case.closed == '04/28/2016'
    assert case.county == 'cleveland'
    assert case.year == '2016'
    assert case.type == 'CF'


def test_live_counts():
    case1 = oscn.request.Case('tulsa-CF-2012-255')
    counts = case1.counts
    assert len(counts) == 3
    assert counts[0]['offense'] == '01/09/2012'
    assert counts[1]['description'] == 'CHILD ABUSE BY INJURY(CHAB)'
    assert counts[1]['violation'] == '21 O.S. 843.5 (A)'
    assert counts[2]['party'] == 'GRAUBERGER, JAIMIE'
    assert counts[2]['disposed'] == 'DEFERRED, 08/28/2012. Guilty Plea'


def test_live_counts_list():
    cases = oscn.request.CaseList(start=15, stop=17)
    for case in cases:
        assert case.counts[0]['party']
