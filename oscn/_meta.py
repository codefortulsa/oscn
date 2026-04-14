import requests
from requests.exceptions import ConnectionError

import functools

from selectolax.parser import HTMLParser

from .settings import (
    OSCN_SEARCH_URL,
    OSCN_REQUEST_HEADER,
    OSCN_PARTY_URL,
    OSCN_APPLICATION_URL,
    OSCN_DOCKETS_URL,
    ALL_COURTS,
    ALL_JUDGES,
    ALL_TYPES,
)


def search_get(**kwargs):
    try:
        response = requests.get(
            OSCN_SEARCH_URL, kwargs, headers=OSCN_REQUEST_HEADER, verify=False
        )
    except ConnectionError:
        return ""
    return response


def party_get(id, db="oklahoma"):
    party_params = {"db": db, "id": id}
    try:
        response = requests.get(
            OSCN_PARTY_URL, party_params, headers=OSCN_REQUEST_HEADER, verify=False
        )
    except ConnectionError:
        return ""
    return response


def docket_get(judge_id, start_date):

    params = {
        "report": "WebJudicialDocketJudgeAll",
        "errorcheck": "true",
        "Judge": judge_id,
        "database": "",
        "db": "Oklahoma",
        "StartDate": start_date,
        "GeneralNumber": "1",
        "generalnumber1": "1",
        "GeneralCheck": "on",
    }

    try:
        response = requests.get(
            OSCN_APPLICATION_URL, params, headers=OSCN_REQUEST_HEADER, verify=False
        )
    except ConnectionError:
        return ""
    return response


@functools.lru_cache()
def courts():
    try:
        response = requests.get(
            OSCN_DOCKETS_URL,
            headers=OSCN_REQUEST_HEADER,
            verify=False,
        )
        tree = HTMLParser(response.text)
        select = tree.css_first('form[action="Results.aspx"] select#db')
        options = select.css("option")
        court_vals = [o.attributes.get("value", "") for o in options]
        court_vals = [v for v in court_vals if v and v != "all"]
        return court_vals
    except:
        return ALL_COURTS


@functools.lru_cache()
def judges():
    try:
        response = requests.get(
            OSCN_APPLICATION_URL + "?report=WebJudicialDocketJudgeAll",
            headers=OSCN_REQUEST_HEADER,
            verify=False,
        )
        tree = HTMLParser(response.text)
        select = tree.css_first("form select")
        options = select.css("option")
        judges_dict = [
            {"number": o.attributes.get("value", ""), "name": o.text().strip()}
            for o in options
        ]
        return judges_dict
    except:
        return ALL_JUDGES


def get_type(type_code):
    get_type = ALL_TYPES.get(type_code, "")
    return get_type


def all_types():
    return ALL_TYPES
