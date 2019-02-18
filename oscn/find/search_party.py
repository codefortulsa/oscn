
import requests
import warnings

from requests.exceptions import ConnectionError

from .. import settings
from .parse import cases

oscn_url = settings.OSCN_SEARCH_URL

# http://www.oscn.net/dockets/Results.aspx
# ?db=all&number=2018-1&lname=&fname=&mname=&DoBMin=&DoBMax=&partytype=&apct=&dcct=&FiledDateL=&FiledDateH=&ClosedDateL=&ClosedDateH=&iLC=&iLCType=&iYear=&iNumber=&citation=


def _request(**kwargs):
    params = {  'db': self.county,
                'lname': self.last,
                'fname':self.first,
                'mname': self.middle
            }
    try:
        response = (
            requests.post(
                oscn_url, params, headers=self.headers, verify=False
            )
        )
    except ConnectionError:
        return self._request(attempts_left=attempts_left-1)

    if response.ok:
        self.text = response.text



def index(index):


class party(object):
    headers = settings.OSCN_REQUEST_HEADER
    response = False

    def __init__(self, county='all', first='', last='', middle='', **kwargs):
        self.county = county
        self.first = first
        self.last = last
        self.middle = middle
            self._request()


# db=all&number=&lname=Bertch&fname=&mname=&DoBMin=&DoBMax=&partytype=&apct=&dcct=&FiledDateL=&FiledDateH=&ClosedDateL=&ClosedDateH=&iLC=&iLCType=&iYear=&iNumber=&citation=
