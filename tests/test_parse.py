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

def test_docket():
    case1 = oscn.request.Case('tulsa-CF-2019-03')
    docket = case1.docket
    assert isinstance(docket, list)
    for minute in docket:
        assert isinstance(minute, dict)
        assert minute['date'] is not ''


def test_issues():
    case1 = oscn.request.Case('tulsa-CV-2019-13')
    issues = oscn.parse.issues(case1.text)

    assert isinstance(issues, list)
    for issue in issues:
        assert isinstance(issue, dict)


def test_parties():
    case1 = oscn.request.Case('tulsa-CJ-2016-143')
    issues = oscn.parse.issues(case1.text)
    assert isinstance(issues, list)
    for issue in issues:
        assert isinstance(issue, dict)
        assert isinstance(issue['parties'], list)
        for party in issue['parties']:
            assert isinstance(party, dict)
            assert 'name' in party.keys()
            assert 'disposed' in party.keys()


def test_attorneys():
    case1 = oscn.request.Case('tulsa-CJ-2016-143')
    attorneys1 = oscn.parse.attorneys(case1.text)

    assert isinstance(attorneys1, list)
    assert len(attorneys1) == 1
    assert attorneys1[0]['representing'] == 'BANK OF AMERICA NA,'

    case2 = oscn.request.Case('mayes-PO-2015-1')
    attorneys2 = oscn.parse.attorneys(case2.text)

    assert isinstance(attorneys2, list)
    assert len(attorneys2) == 0


def test_issue_list():
    case_list = oscn.request.CaseList(counties=['tulsa','oklahoma' 'mayes'], types=['CJ', 'PB', 'CV'], stop=20)

    for case in case_list:
        assert isinstance(case.issues, list)
        for issue in case.issues:
            assert isinstance(issue, dict)
            assert isinstance(issue['parties'], list)
            for party in issue['parties']:
                assert isinstance(party, dict)
                assert 'name' in party.keys()
                assert 'disposed' in party.keys()
