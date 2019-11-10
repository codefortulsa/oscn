import datetime
import requests

from requests.exceptions import ConnectionError

from .. import settings
from .._meta import courts
from .parse import get_case_indexes

OSCN_URL = settings.OSCN_SEARCH_URL
OSCN_HEADER = settings.OSCN_REQUEST_HEADER

# OSCN search wildcards '%' and '_'
# %  Smi%
# _ Sm_th

SEARCH_PARAMS = {
    "db" : "all",
    "number" : "",
    "lname" : "",
    "fname" : "",
    "mname" : "",
    "DoBMin" : "",
    "DoBMax" : "",
    "partytype" : "",
    "apct" : "",
    "dcct" : "",
    "FiledDateL" : "01/01/2019",
    "FiledDateH" : "",
    "ClosedDateL" : "",
    "ClosedDateH" : "",
    "iLC" : "",
    "iLCType" : "",
    "iYear" : "",
    "iNumber" : "",
    "citation" : "",
}


def ask_oscn(**kwargs):
    try:
        response = (
            requests.post(
                OSCN_URL, kwargs, headers=OSCN_HEADER, verify=False
            )
        )
    except ConnectionError:
        return ""

    return response

def add_wildcards(name_str):
    "%25".join(name.split())


class CaseIndexes(object):
    def __init__(self, county="all",
                 last="",
                 first="",
                 middle="",
                 filed_after="",
                 filed_before="",
                 closed_after="",
                 closed_before="",
                 **kwargs):
        add_wildcards = lambda nm:"%25".join(nm.split())
        self.search =  SEARCH_PARAMS.copy()
        self.search['db']=county
        self.search['lname'] = add_wildcards(last)
        self.search['fname'] = add_wildcards(first)
        self.search['mname'] = add_wildcards(middle)
        self.search["FiledDateL" ] = filed_after
        self.search["FiledDateH" ] = filed_before
        self.search["ClosedDateL"] = closed_after
        self.search["ClosedDateH"] = closed_before


        for kw in kwargs:
            if kw in self.search.keys():
                self.search[kw]=kwargs[kw]

        results = ask_oscn(**self.search)
        self.text = results.text
        self.source = f'{results.request.url}?{results.request.body}'
        self._indexes = self._case_indexes()


    def __iter__(self):
        return self

    def __next__(self):
        return next(self._indexes)

    def _case_indexes(self):
        cases = get_case_indexes(self.text)
        skip_county = ''
        for case_index in cases:
            county, type = case_index.split('-')[:2]
            if type == 'more':
                skip_county = county
                county_search = self.search.copy()
                county_search['db'] = county
                county_results = ask_oscn(**county_search)
                county_cases = get_case_indexes(county_results.text)
                for county_idx in county_cases:
                    yield county_idx
            else:
                if county != skip_county:
                    yield case_index
