import oscn


def test_find_name():
    # cases = oscn.find.cases(name="smith", first="bob")
    #
    # import ipdb; ipdb.set_trace()

    # cases = oscn.find.cases(name="AMERICAN EXPRESS")
    cases = oscn.find.CaseIndexes(name="DISCOVER BANK")

    for case in cases:
        print(case)

    import ipdb; ipdb.set_trace()
    pass
