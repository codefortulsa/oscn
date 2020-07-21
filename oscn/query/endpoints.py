import requests

from decouple import config

# https://stage.oscn.net/swagger/#/

OSCN_API_URL = "https://stage.oscn.net/api"

OSCN_API_HEADER = {"accept": "application/json; charset=utf-8"}

OSCN_API_ACCESS_KEY = config('OSCN_API_ACCESS_KEY')


class api_request(object):
    access_key = {"k": OSCN_API_ACCESS_KEY, }

    def __init__(self, **kwargs):
        pass

    def __call__(self, **kwargs):
        requestor = getattr(requests, self.type)
        q_json = kwargs.pop("q", None)
        params = {**self.access_key, **kwargs}
        try:
            response = requestor(
                f"{OSCN_API_URL}/{self.endpoint}",
                json=q_json,
                params=params,
                headers=OSCN_API_HEADER,
                verify=False
                )
        except Exception as e:
            return e
        return response


# es queries
class query_request(api_request):
    endpoint = "ocis_cases"
    type = "post"
    required_params = ['q']


query = query_request()


class updates_request(api_request):
    endpoint = "ocis_updates"
    type = "get"


updates = updates_request()


#  requests for single case
class dockets_request(api_request):
    endpoint = "dockets"
    type = "get"
    required_params = ['county', 'cn']


dockets = dockets_request()


class events_request(api_request):
    endpoint = "events"
    type = "get"
    required_params = ['county', 'cn']


events = events_request()


class style_request(api_request):
    endpoint = "style"
    type = "get"
    required_params = ['county', 'cn']


style = style_request()


class counts_request(api_request):
    endpoint = "counts"
    type = "get"
    required_params = ['county', 'cn']


counts = counts_request()


class parties_request(api_request):
    endpoint = "parties"
    type = "get"
    required_params = ['county', 'cn']


parties = parties_request()


class attorneys_request(api_request):
    endpoint = "attorneys"
    type = "get"
    required_params = ['county', 'cn']


attorneys = attorneys_request()

