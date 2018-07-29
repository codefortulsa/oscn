import requests
import warnings

from . import settings

from oscn.parse import append_parsers

oscn_url = settings.OSCN_URL
warnings.filterwarnings("ignore")


class OSCNrequest(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
        }

    def __init__(self, type='CF', county='tulsa', year='2018', number=1):
        self.type = type
        self.county = county
        self.year = year
        self.number = number

    @property
    def case_number(self):
        return f'{self.type}-{self.year}-{self.number}'

    @property
    def source(self):
        return f'{oscn_url}?db={self.county}&number={self.case_number}'

    @property
    def text(self):
        return self.response.text

    def _valid_response(self, resp):
        if resp.status_code != 200:
            return False
        for msg in settings.INVALID_CASE_MESSAGES:
            if msg in resp.text:
                return False
        return True

    def _request(self):
        params = {'db': self.county, 'number': self.case_number}
        response = (
            requests.post(oscn_url, params, headers=self.headers, verify=False)
            )
        if self._valid_response(response):
            self.response = response
            return self
        else:
            return None

# This next section adds properties to the OSCNrequest as a shortcut
# for parsing.  This allows access to parse results such as:
# name = OSCNrequest.judge
# or
# counts = OSCNrequest.counts

append_parsers(OSCNrequest)

class Case(OSCNrequest):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._request()


class CaseList(OSCNrequest):

    def __init__(self, start=0, stop=False, **kwargs):
        number = start if start==0 else start-1
        self.start = start
        self.stop = stop
        super().__init__(number=number, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        self.number += 1
        if self.stop and self.number > self.stop:
            raise StopIteration
        next_case = self._request()
        if next_case:
            for msg in settings.UNUSED_CASE_MESSAGES:
                if msg in next_case.response.text:
                    self.number += 1
                    return self.__next__()
            return next_case
        else:
            raise StopIteration
