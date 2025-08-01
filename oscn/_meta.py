import requests
from requests.exceptions import ConnectionError

import functools

from bs4 import BeautifulSoup

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
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form", action="Results.aspx")
        select = form.find("select", id="db")
        options = select.find_all("option")
        court_vals = [option["value"] for option in options]
        court_vals.remove("all")
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
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form")
        select = form.find("select")
        options = select.find_all("option")
        judge_numbers = [option["value"] for option in options]
        judge_names = [option.text for option in options]
        judges_dict = [
            {"number": num, "name": name}
            for num, name in zip(judge_numbers, judge_names)
        ]
        return judges_dict

    except:
        return ALL_JUDGES


def get_type(type_code):
    get_type = ALL_TYPES.get(type_code, "")
    return get_type


def all_types():
    return ALL_TYPES
