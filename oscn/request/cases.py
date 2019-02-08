
import os, errno
import gzip
import json

from types import FunctionType

import logging
import requests
import warnings

from requests.exceptions import ConnectionError

from .. import settings

from ..parse import append_parsers
from ..find import append_finders

oscn_url = settings.OSCN_URL
warnings.filterwarnings("ignore")
logger = logging.getLogger('oscn')

logger.setLevel(logging.INFO)

class Case(object):
    headers = settings.OSCN_REQUEST_HEADER
    response = False

    def __init__(
            self, type='CF', county='tulsa', year='2019', number=1, **kwargs):
        self.type = type
        self.county = county
        self.year = year
        self.number = number
        self.cmid = kwargs['cmid'] if 'cmid' in kwargs else False
        self.directory = kwargs['directory'] if 'directory' in kwargs else ''

        if self.directory:
            self._open(self.directory)
        else:
            self._request()

    @property
    def case_number(self):
        if self.cmid:
            return f'cmid:{self.cmid}'
        else:
            return f'{self.type}-{self.year}-{self.number}'

    @property
    def case_index(self):
        return f'{self.county}-{self.case_number}'

    @property
    def path(self):
        return f'{self.directory}/{self.county}/{self.year}/{self.type}/'

    def save(self, directory=''):
        case_data = {
            'source': self.source,
            'county': self.county,
            'type': self.type,
            'year': self.year,
            'number': self.number,
            'text': self.text,
        }
        file_name = f'{directory}/{self.path}/{self.number}.json'
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with gzip.GzipFile(file_name, 'w') as open_file:
            open_file.write(json.dumps(case_data).encode('utf-8'))

    def _open(self, directory=''):
        file_name = f'{self.path}/{self.number}.json'
        try:
            with gzip.GzipFile(file_name, 'r') as open_file:
                saved_data = json.loads(open_file.read().decode('utf-8'))
                self.source = saved_data['source']
                self.county = saved_data['county']
                self.type = saved_data['type']
                self.year = saved_data['year']
                self.number = saved_data['number']
                self.text = saved_data['text']
            self.valid = True
        except FileNotFoundError:
            self.valid = False

    def _valid_response(self, response):
        if not response.ok:
            return False
        for msg in settings.INVALID_CASE_MESSAGES:
            if msg in response.text:
                logger.info("Case %s is invalid", self.case_number)
                return False
        return True

    def _request(self, attempts_left=settings.MAX_EMPTY_CASES):

        if self.cmid:
            params = {'db': self.county, 'cmid': self.cmid}
        else:
            params = {'db': self.county, 'number': self.case_number}

        try:
            response = (
                requests.post(
                    oscn_url, params, headers=self.headers, verify=False
                )
            )
        except ConnectionError:
            return self._request(attempts_left=attempts_left-1)

        if self._valid_response(response):
            self.valid = True
            self.source = f'{response.url}?{response.request.body}'
            self.text = response.text
            for msg in settings.UNUSED_CASE_MESSAGES:
                if msg in response.text:
                    self.number += 1
                    if attempts_left > 0:
                        logger.info("Case %s might be last, trying %d more",
                                    self.case_number, attempts_left)
                        return self._request(attempts_left=attempts_left-1)
                    else:
                        self.valid = False
                        return
            logger.info("Case %s fetched", self.case_number)
        else:
            self.valid = False


# This next line adds properties to the OSCNrequest as a shortcut
# for parsing.  This allows access to parse results such as:
# name = Case.judge
# or
# counts = Case.counts
append_parsers(Case)
append_finders(Case)


class CaseFilter(object):

    def __init__(self, target, test):
        # target is the property of a case to be tested
        self.target = target
        # test is a function used to evaluate the target values
        if isinstance(test, FunctionType):
            self.test = test
        # turn a str into a function to find the str in the target value
        elif isinstance(test, str):
            self.test = lambda val: test in val


class CaseList(object):
    filters = []

    def _passes_filters(self, case_to_test):
        # no filters? you pass!
        if self.filters == []:
            return True

        # make a list of filters that match properties on case_to_test
        case_props = dir(case_to_test)
        is_prop = lambda f: f.target in case_props
        test_filters = [f for f in filter(is_prop, self.filters)]

        # no filters found? you pass!
        if test_filters == []:
            return True

        # make a list of functions and a list of values
        filter_funcs = [f.test for f in test_filters]
        case_values = [getattr(case_to_test, f.target) for f in test_filters]

        # run the tests
        does_it_pass = lambda fn, val: fn(val)
        test_results = map(does_it_pass, filter_funcs, case_values)

        # see if they are all true
        return all(test_results)

    def _request_generator(self):
        for case_type in self.types:
            for county in self.counties:
                for year in self.years:
                    self.number = self.start
                    while True:
                        if self.stop and self.number > self.stop:
                            break
                        next_case = Case(number=self.number,
                                         type=case_type,
                                         county=county,
                                         year=year)
                        self.number = next_case.number+1
                        if next_case.valid:
                            if next_case.cmids:
                                for cmid in next_case.cmids:
                                    cmid_case = Case(county=county, cmid=cmid)
                                    if cmid_case.response:
                                        if self._passes_filters(cmid_case):
                                            yield cmid_case
                            else:
                                if self._passes_filters(next_case):
                                        yield next_case
                        else:
                            break
        raise StopIteration

    def _file_generator(self, directory):
        for case_type in self.types:
            for county in self.counties:
                for year in self.years:
                    self.number = self.start
                    first_case = Case(number=self.number,
                                        type=case_type,
                                        county=county,
                                        year=year,
                                        directory=directory)
                    if first_case.valid:
                        if self._passes_filters(first_case):
                                yield first_case
                    max_cases= len(os.listdir(first_case.path))
                    self.number = first_case.number+1
                    while self.number <= max_cases:
                        if self.stop and self.number > self.stop:
                            break
                        next_case = Case(number=self.number,
                                            type=case_type,
                                            county=county,
                                            year=year,
                                            directory=directory)
                        count_cases= len(os.listdir(next_case.path))
                        self.number = next_case.number+1
                        if next_case.valid:
                            if self._passes_filters(next_case):
                                    yield next_case
                        else:
                            max_cases += 1
        raise StopIteration

    def __init__(self,
                 types=['CF', 'CM'],
                 counties=['tulsa', 'oklahoma'],
                 years=['2018', '2017'],
                 start=1, stop=False, **kwargs):

        self.start = start
        self.stop = stop

        # this next section allows passing single arguments, such as
        # type = 'CM' or county = 'tulsa' or year = '2018'
        # it also allows passing a list with these argumens, such as
        # year=['2018','2017']

        # make a str into a single element list otherwise return the value
        str_to_list = lambda val: [val] if type(val) is str else val

        # use the default value if type, county, or year aren't passed
        self.types = str_to_list(kwargs['type']) if 'type' in kwargs else types
        self.counties = (
            str_to_list(kwargs['county']) if 'county' in kwargs else counties)
        self.years = str_to_list(kwargs['year']) if 'year' in kwargs else years

        # create the generator for this list
        if 'directory' in kwargs:
            self.all_cases = self._file_generator(kwargs['directory'])
        else:
            self.all_cases = self._request_generator()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.all_cases)

    def find(self, **kwargs):
        for kw in kwargs:
            self.filters.append(CaseFilter(kw, kwargs[kw]))
        return self
