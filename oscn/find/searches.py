import datetime
import requests

from enum import Enum

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
    "FiledDateL" : "01/01/2020",
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

class OSCN_SearchParams(Enum):
    county = "db"
    last_name = "lname"
    first_name = "fname"
    middle_name = "mname"
    filed_after = "FiledDateL"
    filed_before = "FiledDateH"
    closed_after = "ClosedDateL"
    closed_before = "ClosedDateH"


class CaseIndexes(object):
    def __init__(self, **kwargs):
        self.search =  SEARCH_PARAMS.copy()
        for kw in kwargs.keys():
            if kw in OSCN_SearchParams.__members__:
                oscn_param = OSCN_SearchParams[kw].value
                self.search[oscn_param]=kwargs[kw]
            elif kw in self.search.keys():
                self.search[kw]=kwargs[kw]


        name_params = ['lname', 'fname', 'mname']
        add_wildcards = lambda nm:"%25".join(nm.split())
        for param in name_params:
            self.search[param] = add_wildcards(self.search[param])

        if 'text' in kwargs.keys():
            self.text = kwargs['text']
            self.source = ""
        else:
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
