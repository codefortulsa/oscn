import logging
import requests
import warnings

from . import settings

from oscn.parse import append_parsers

oscn_url = settings.OSCN_URL
warnings.filterwarnings("ignore")
logger = logging.getLogger('oscn')


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
                logger.info("Case %s is invalid", self.case_number)
                return False
        return True

    def _request(self, attempts_left=settings.MAX_EMPTY_CASES):
        params = {'db': self.county, 'number': self.case_number}
        response = (
            requests.post(oscn_url, params, headers=self.headers, verify=False)
            )
        if self._valid_response(response):
            for msg in settings.UNUSED_CASE_MESSAGES:
                if msg in response.text:
                    self.number += 1
                    if attempts_left > 0:
                        logger.info("Case %s might be last, trying %d more", self.case_number, attempts_left)
                        return self._request(attempts_left=attempts_left-1)
                    else:
                        return None
            logger.info("Case %s fetched", self.case_number)
            self.response = response
            return self
        else:
            return None

# This next line adds properties to the OSCNrequest as a shortcut
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
    filters = []

    def _convert_str_arg(self, name, args):
        if name in args:
            if type(args[name]) is str:
                # convert str to one element list
                args[name] = [args[name]]

    def pass_filter(self):
        if self.filters == []:
            return True
        for fltr in self.filters:
            test_value = getattr(self, fltr['name'])
            if fltr['test'](test_value):
                return True
        return False

    def _gen_requests(self):
        for county in self.counties:
            self.county = county
            for year in self.years:
                self.year = year
                self.number = self.start
                while True:
                    self.number += 1
                    if self.stop and self.number > self.stop:
                        break
                    next_case = self._request()
                    if next_case:
                        if self.pass_filter():
                            yield next_case
                    else:
                        break
        raise StopIteration

    def __init__(self, start=0, stop=False, **kwargs):
        self.start = start if start == 0 else start-1
        self.stop = stop
        self._convert_str_arg('county', kwargs)
        self._convert_str_arg('year', kwargs)
        self.counties = kwargs['county']
        self.years = kwargs['year']
        self.all_cases = self._gen_requests()
        super().__init__(number=self.start, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.all_cases)

    def find(self, **kwargs):
        # see if any kwargs match self attr
        attrs = dir(self)
        is_prop = lambda kw: kw in attrs
        for kw in filter(is_prop, kwargs):
            self.filters.append({'name': kw, 'test': kwargs[kw]})
