
import os, errno
from io import BytesIO
import gzip
import json

from types import FunctionType

import logging
import warnings

import requests
from requests.exceptions import ConnectionError

import boto3
import botocore
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

from .. import settings

from ..parse import append_parsers

oscn_url = settings.OSCN_CASE_URL
warnings.filterwarnings("ignore")
logger = logging.getLogger('oscn')

logger.setLevel(logging.INFO)

class Case(object):
    headers = settings.OSCN_REQUEST_HEADER
    response = False

    def __init__(self, index=False, type='CF', county='tulsa', year='2019', number=1, **kwargs):
        if index:
            county, type, year, number = index.split('-')
        self.type = type
        self.county = county
        self.year = year
        self.number = number
        self.cmid = kwargs['cmid'] if 'cmid' in kwargs else False
        self.directory = kwargs['directory'] if 'directory' in kwargs else ''
        self.bucket = kwargs['bucket'] if 'bucket' in kwargs else ''
        if self.directory:
            self._open_file()
        elif self.bucket:
            self._open_s3_object()
        else:
            self._request()

    @property
    def oscn_number(self):
        if self.cmid:
            return f'cmid:{self.cmid}'
        else:
            return f'{self.type}-{self.year}-{self.number}'

    @property
    def index(self):
        return f'{self.county}-{self.oscn_number}'

    @property
    def path(self):
        return f'{self.directory}/{self.county}/{self.year}/{self.type}'

    @property
    def file_name(self):
        return f'{self.path}/{self.number}.case'

    @property
    def s3_key(self):
        return f'{self.county}/{self.year}/{self.type}/{self.number}.case'

    def save(self, **kwargs):
        case_data = {
            'source': self.source,
            'county': self.county,
            'type': self.type,
            'year': self.year,
            'number': self.number,
            'text': self.text,
        }
        file_data = gzip.compress(bytes(json.dumps(case_data),'utf-8'))

        self.directory = kwargs['directory'] if 'directory' in kwargs else ''
        self.bucket = kwargs['bucket'] if 'bucket' in kwargs else ''
        if self.directory:
            if not os.path.exists(os.path.dirname(self.file_name)):
                try:
                    os.makedirs(os.path.dirname(self.file_name))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(self.file_name, 'wb') as open_file:
                open_file.write(file_data)

        elif self.bucket:
            try:
                s3.meta.client.head_bucket(Bucket=self.bucket)
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404' or error_code == '403':
                    s3.create_bucket(Bucket=self.bucket)
                else:
                    raise e
            s3.Bucket(self.bucket).put_object(Key=self.s3_key, Body=file_data)

    def _open_file(self):
        try:
            with gzip.GzipFile(self.file_name, 'r') as open_file:
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

    def _open_s3_object(self):
        try:
            s3_object = s3_client.get_object(Bucket=self.bucket, Key=self.s3_key)
            bytestream = BytesIO(s3_object['Body'].read())
            unzipped_stream = gzip.GzipFile(None, 'rb', fileobj=bytestream).read().decode('utf-8')
            saved_data = json.loads(unzipped_stream)
            self.source = saved_data['source']
            self.county = saved_data['county']
            self.type = saved_data['type']
            self.year = saved_data['year']
            self.number = saved_data['number']
            self.text = saved_data['text']
            self.valid = True
        except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'NoSuchKey':
                    self.valid = False
                else:
                    raise e

    def _valid_response(self, response):
        if not response.ok:
            return False
        for msg in settings.INVALID_CASE_MESSAGES:
            if msg in response.text:
                logger.info("Case %s is invalid", self.oscn_number)
                return False
        return True

    def _request(self, attempts_left=settings.MAX_EMPTY_CASES):
        if self.cmid:
            params = {'db': self.county, 'cmid': self.cmid}
        else:
            params = {'db': self.county, 'number': self.oscn_number}

        try:
            response = (
                requests.post(
                    oscn_url, params, headers=self.headers, verify=False
                )
            )
        except ConnectionError:
            if attempts_left > 0:
                return self._request(attempts_left=attempts_left-1)
        if self._valid_response(response):
            self.valid = True
            self.source = f'{response.url}?{response.request.body}'
            self.text = response.text
            for msg in settings.UNUSED_CASE_MESSAGES:
                if msg in response.text:
                    self.valid = False
                    return
        else:
            self.valid = False


# This next line adds properties to the OSCNrequest as a shortcut
# for parsing.  This allows access to parse results such as:
# name = Case.judge
# or
# counts = Case.counts
append_parsers(Case)


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

    def _index_generator(self, start, stop):
        case_numbers = range(start, stop+1)
        for county in self.counties:
            for year in self.years:
                for case_type in self.types:
                    self.exit_type = False
                    for num in case_numbers:
                        yield (f'{county}-{case_type}-{year}-{num}')
                        if self.exit_type:
                            break
        raise StopIteration

    def _request_generator(self):
        request_attempts=10
        for index in self.case_indexes:
            case = Case(index)
            if case.valid:
                if case.cmids:
                    for cmid in case.cmids:
                        cmid_case = Case(county=county, cmid=cmid)
                        if cmid_case.response:
                            if self._passes_filters(cmid_case):
                                yield cmid_case
                else:
                    request_attempts=10
                    if self._passes_filters(case):
                        yield case
            else:
                if request_attempts > 0:
                    request_attempts -= 1
                else:
                    self.exit_type = True
        raise StopIteration

    def _file_generator(self, directory):
        open_attempts = 10
        for index in self.case_indexes:
            case = Case(index=index, directory=directory)
            if case.valid:
                open_attempts = 10
                if self._passes_filters(case):
                        yield case
            else:
                if open_attempts > 0:
                    open_attempts -= 1
                else:
                    self.exit_type = True
        raise StopIteration

    def _s3_generator(self, bucket):
        open_attempts = 10
        for index in self.case_indexes:
            case = Case(index=index, bucket=bucket)
            if case.valid:
                open_attempts = 10
                if self._passes_filters(case):
                        yield case
            else:
                if open_attempts > 0:
                    open_attempts -= 1
                else:
                    self.exit_type = True
        raise StopIteration

    def __init__(self,
                 types=['CF', 'CM'],
                 counties=['tulsa', 'oklahoma'],
                 years=['2018', '2017'],
                 start=1, stop=20000, **kwargs):

        self.start = start
        self.stop = stop

        # this next section allows passing single arguments, such as
        # type = 'CM' or county = 'tulsa' or year = '2018'
        # it also allows passing a list with these arguments, such as
        # year=['2018','2017']

        # make a str into a single element list otherwise return the value
        str_to_list = lambda val: [val] if type(val) is str else val

        # use the default value if type, county, or year aren't passed
        self.types = str_to_list(kwargs['type']) if 'type' in kwargs else types
        self.counties = (
            str_to_list(kwargs['county']) if 'county' in kwargs else counties)
        self.years = str_to_list(kwargs['year']) if 'year' in kwargs else years

        # create all arguments
        self.case_indexes = self._index_generator(start, stop)

        # create the generator for this list
        if 'directory' in kwargs:
            self.all_cases = self._file_generator(kwargs['directory'])
        elif 'bucket' in kwargs:
            self.all_cases = self._s3_generator(kwargs['bucket'])
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
