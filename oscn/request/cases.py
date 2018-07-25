import requests
import warnings

from . import settings

from oscn.parse import judge, parties, counts, docket

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

# This next section adds properties to the OSCNrequest as a shortcuts
# for parsing.  This allows access to parse results such as:
# name = OSCNrequest.judge
# or
# counts = OSCNrequest.counts

# These parsing functions were imported from the parse module above.
case_parsers = [judge, counts, parties, docket]

# this function accepts a function and returns a property
# the lambda is the 'fget' function of the property
#  which returns the result of the parse_function using
#  the response.text of the object instance
def make_property(parse_function):
    return property(lambda self: parse_function(self.response.text))

for parser in case_parsers:
    # This adds an attribute to OSCNrequest with the name of the parser
    # and a new property created using the parser function
    setattr(OSCNrequest, parser.__name__, make_property(parser))

class Case(OSCNrequest):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._request()


class CaseList(OSCNrequest):

    def __init__(self, **kwargs):
        super().__init__(number=0, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        self.number += 1
        next_case = self._request()
        if next_case:
            for msg in settings.UNUSED_CASE_MESSAGES:
                if msg in next_case.response.text:
                    self.number += 1
                    return self.__next__()
            return next_case
        else:
            raise StopIteration
