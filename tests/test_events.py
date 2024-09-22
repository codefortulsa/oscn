import oscn


def test_events():
    case = oscn.request.Case("tulsa-FD-2022-945")    
    events = case.events
    first = events[0]
    # {'date': 'Wednesday, May 25, 2022 at 9:30 AM', 'description': 'Parenting Plan Conference'},
    assert first['date'] == 'Wednesday, May 25, 2022 at 9:30 AM'
    assert first['description'] == 'Parenting Plan Conference'

    case = oscn.request.Case("tulsa-FD-2016-3013")
    events = case.events
    second = events[1]
    # {'date': 'Thursday, January 5, 2017 at 9:00 AM', 'description': 'Parenting Plan Conference'}
    assert second['date'] ==  'Thursday, January 5, 2017 at 9:00 AM'
    assert second['description'] == 'Parenting Plan Conference'
    
