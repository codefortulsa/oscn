import oscn


def test_body_text():
    case = oscn.request.Case("cleveland-CF-2016-84")

    body_text = case.body

    assert isinstance(body_text, str)
    assert "Judge: Walkley, Lori" in body_text
    assert "<div" not in body_text
