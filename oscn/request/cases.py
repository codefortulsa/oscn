from types import FunctionType

import logging
import requests
import warnings

from . import settings

from ..parse import append_parsers

oscn_url = settings.OSCN_URL
warnings.filterwarnings("ignore")
logger = logging.getLogger('oscn')


class Case(object):
    headers = settings.OSCN_REQUEST_HEADER

    def __init__(self, type='CF', county='tulsa', year='2018', number=1):
        self.type = type
        self.county = county
        self.year = year
        self.number = number
        self._request()

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
                        logger.info("Case %s might be last, trying %d more",
                                    self.case_number, attempts_left)
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
# name = Case.judge
# or
# counts = Case.counts

append_parsers(Case)


class CaseList(object):
    filters = []

    def _passes_filters(self, case_to_test):
        # no filters? you pass!
        if self.filters == []:
            return True

        # make a list of filters that match properties on case_to_test
        case_attrs = dir(case_to_test)
        is_prop = lambda fl: fl['attr_name'] in case_attrs
        test_filters = [f for f in filter(is_prop, self.filters)]

        # no filters found? you pass!
        if test_filters == []:
            return True

        # make a list of functions and a list of values
        filter_funcs = [case_filter['test'] for case_filter in test_filters]
        case_values = [getattr(case_to_test, case_filter['attr_name'])
                       for case_filter in test_filters]

        # run the tests
        does_it_pass = lambda fn, val: fn(val)
        test_results = map(does_it_pass, filter_funcs, case_values)

        # see if they are all true
        return all(test_results)

    def _gen_requests(self):
        for case_type in self.types:
            for county in self.counties:
                for year in self.years:
                    self.number = self.start
                    while True:
                        self.number += 1
                        if self.stop and self.number > self.stop:
                            break
                        next_case = Case(number=self.number,
                                         type=case_type,
                                         county=county,
                                         year=year)
                        if next_case:
                            if self._passes_filters(next_case):
                                yield next_case
                        else:
                            break
        raise StopIteration

    def __init__(self,
                 types=['CF', 'CM'],
                 counties=['tulsa', 'oklahoma'],
                 years=['2018', '2017'],
                 start=0, stop=False, **kwargs):

        self.start = start if start == 0 else start-1
        self.stop = stop

        # this next section allows passing single arguments, such as
        # type = 'CM' or county = 'tulsa' or year = '2018'
        # it also allows passing a list with these argumens, such as
        # year=['2018','2017']


        # make a str into a single element list otherwise return the value
        # use the default value if type, county, or year aren't passed
        mk_list = lambda val: [val] if type(val) is str else val
        self.types = mk_list(kwargs['type']) if 'type' in kwargs else types
        self.counties = (
            mk_list(kwargs['county']) if 'county' in kwargs else counties)
        self.years = mk_list(kwargs['year']) if 'year' in kwargs else years

        # create the generator for this list
        self.all_cases = self._gen_requests()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.all_cases)

    def find(self, **kwargs):
        for kw in kwargs:
            if isinstance(kwargs[kw], FunctionType):
                attr_test = kwargs[kw]
            elif isinstance(kwargs[kw], str):
                attr_test = lambda val: kwargs[kw] in val
            self.filters.append({'attr_name': kw, 'test': attr_test})
        return self
