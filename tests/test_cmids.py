import oscn
from oscn.parse.lax_cmids import cmids
from oscn.parse.bs4_cmids import bs4_cmids

def test_retrieve_parent_and_cmids():
    parent_case_index = "johnston-CF-2011-00015"

    parent_case = oscn.request.Case(parent_case_index)
    html = parent_case.text
    # use bs4
    bs4_result = bs4_cmids(html)
    assert len(bs4_result) == 4
    
    # use lax
    cmids_result = cmids(html)
    assert len(cmids_result) == 4

    assert bs4_result == cmids_result

