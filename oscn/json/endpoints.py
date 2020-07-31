import requests
import json


from ..settings import OSCN_API_HEADER, OSCN_API_URL, OSCN_API_ACCESS_KEY


class api_request(object):
    access_key = {
        "k": OSCN_API_ACCESS_KEY,
    }

    def __call__(self, **kwargs):
        case_index = kwargs.get("index", False)
        if case_index:
            index_parts = case_index.split("-")
            county = index_parts.pop(0)
            kwargs["county"] = county
            kwargs["cn"] = "-".join(index_parts)

        requestor = getattr(requests, self.type)
        params = {**self.access_key, **kwargs}
        try:
            response = requestor(
                f"{OSCN_API_URL}/{self.endpoint}",
                params=params,
                headers=OSCN_API_HEADER,
                verify=False,
            )
        except Exception as e:
            return e

        response_dict = json.loads(response.text)
        result = response_dict.get("result", [])
        data = result[0].get("data", [])
        return data


class style_request(api_request):
    endpoint = "style"
    type = "get"
    required_params = ["county", "cn"]


style = style_request()


class nested_response(api_request):
    def __call__(self, **kwargs):
        super_data = super().__call__(**kwargs)
        return super_data[self.endpoint]


class dockets_request(nested_response):
    endpoint = "dockets"
    type = "get"
    required_params = ["county", "cn"]


docket = dockets_request()


class events_request(nested_response):
    endpoint = "events"
    type = "get"
    required_params = ["county", "cn"]


events = events_request()


class counts_request(nested_response):
    endpoint = "counts"
    type = "get"
    required_params = ["county", "cn"]


counts = counts_request()


class parties_request(nested_response):
    endpoint = "parties"
    type = "get"
    required_params = ["county", "cn"]


parties = parties_request()


class attorneys_request(nested_response):
    endpoint = "attorneys"
    type = "get"
    required_params = ["county", "cn"]


attorneys = attorneys_request()
