import os
import re
import errno
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

from .. import settings
from ..parse import append_parsers

s3 = boto3.resource("s3")
s3_client = boto3.client("s3")

oscn_url = settings.OSCN_CASE_URL
warnings.filterwarnings("ignore")
logger = logging.getLogger("oscn")

logger.setLevel(logging.INFO)


# regex for index parsing

get_court = re.compile(r'^(?P<court>\w+)-')
get_type = re.compile(r'-(?P<type>\w+)-')
get_year = re.compile(r'-(?P<year>\d{4})-')
get_number = re.compile(r'0*(?P<number>\d+)$')

# This decorators adds properties to the OSCNrequest as a shortcut
# for parsing.  This allows access to parse results such as:
# name = Case.judge
# or
# counts = Case.counts
@append_parsers
class Case(object):
    headers = settings.OSCN_REQUEST_HEADER
    response = False

    def __init__(
        self,
        index=False,
        type=None,
        county=None,
        year=None,
        number=None,
        cmid=False,
        **kwargs,):
    
        if index:
            self.county = get_court.match(index).group('court')
            self.number = get_number.search(index).group('number')

            try:
                self.type = get_type.search(index).group('type')
            except AttributeError as exc:
                self.type=None

            try:
                self.year = get_year.search(index).group('year')
            except AttributeError as exc:
                self.year=None

        else:
            self.county = county
            self.year = year
            self.number = number
            self.type = type

        if hasattr(self, "type"):
            self.cmid = self.type == "cmid"
        else:
            self.cmid = False

        self.source = kwargs["source"] if "source" in kwargs else False

        if "text" in kwargs:
            self.text = kwargs["text"]
            return self
        else:
            self.directory = kwargs["directory"] if "directory" in kwargs else ""
            self.bucket = kwargs["bucket"] if "bucket" in kwargs else ""
            if self.directory:
                self._open_file()
            elif self.bucket:
                self._open_s3_object()
            else:
                # default for test
                self.text = ""
                self._request()

    @property
    def oscn_number(self):
        key_names = ["type", "year", "number"]
        number_parts = []
        for ky in key_names:
            if hasattr(self, ky):
                ky_val = getattr(self, ky)
                if ky_val:
                    number_parts.append(str(getattr(self, ky)))
        return "-".join(number_parts)

    @property
    def index(self):
        return f"{self.county}-{self.oscn_number}"

    @property
    def inner_path(self):
        path_parts = []
        key_names = ["county", "type", "year"]
        for ky in key_names:
            if hasattr(self, ky):
                path_parts.append(getattr(self, ky))
        return "/".join(path_parts)

    @property
    def path(self):
        return f"{self.directory}/{self.inner_path}"

    @property
    def file_name(self):
        return f"{self.path}/{self.number}.zip"

    @property
    def s3_key(self):
        return f"{self.inner_path}/{self.number}.zip"

    def save(self, **kwargs):
        case_data = {
            "source": self.source,
            "index": self.index,
            "text": self.text,
        }
        file_data = gzip.compress(bytes(json.dumps(case_data), "utf-8"))

        self.directory = kwargs["directory"] if "directory" in kwargs else ""
        self.bucket = kwargs["bucket"] if "bucket" in kwargs else ""
        if self.directory:
            if not os.path.exists(os.path.dirname(self.file_name)):
                try:
                    os.makedirs(os.path.dirname(self.file_name))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(self.file_name, "wb") as open_file:
                open_file.write(file_data)

        if self.bucket:
            try:
                s3.meta.client.head_bucket(Bucket=self.bucket)
            except botocore.exceptions.ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "404" or error_code == "403":
                    s3.create_bucket(Bucket=self.bucket)
                else:
                    raise e
            s3.Bucket(self.bucket).put_object(Key=self.s3_key, Body=file_data)

    def _open_file(self):
        try:
            with gzip.GzipFile(self.file_name, "r") as open_file:
                saved_data = json.loads(open_file.read().decode("utf-8"))
                self.__init__(**saved_data)
            self.valid = True
        except FileNotFoundError:
            self.valid = False

    def _open_s3_object(self):
        try:
            s3_object = s3_client.get_object(Bucket=self.bucket, Key=self.s3_key)
            bytes = BytesIO(s3_object["Body"].read())
            unzipped_stream = (
                gzip.GzipFile(None, "rb", fileobj=bytes).read().decode("utf-8")
            )
            saved_data = json.loads(unzipped_stream)
            self.__init__(**saved_data)
            self.valid = True
        except botocore.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchKey":
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
        params = {"db": self.county}
        if self.cmid:
            params["cmid"] = self.number
        else:
            params["number"] = self.oscn_number

        try:
            response = requests.post(
                oscn_url, params, headers=self.headers, verify=False
            )
        except ConnectionError:
            if attempts_left > 0:
                return self._request(attempts_left=attempts_left - 1)
            else:
                raise ConnectionError

        if self._valid_response(response):
            self.valid = True
            self.source = f"{response.url}"
            self.text = response.text
            for msg in settings.UNUSED_CASE_MESSAGES:
                if msg in response.text:
                    self.valid = False
                    return
        else:
            self.valid = False


class CaseList(object):
    def __init__(self, types=[], counties=[], years=[], start=1, stop=20000, **kwargs):

        self.start = start
        self.stop = stop
        self.filters = []

        # allow kwargs to override certain args
        self.types = kwargs["type"] if "type" in kwargs else types
        self.counties = kwargs["county"] if "county" in kwargs else counties
        self.years = kwargs["year"] if "year" in kwargs else years

        # Allow passing a string to list keywords
        # make a str into a single element list otherwise return the value
        str_to_list = lambda val: [val] if type(val) is str else val
        self.types = str_to_list(self.types)
        self.counties = str_to_list(self.counties)
        self.years = str_to_list(self.years)

        # create case request based on storage option
        if "directory" in kwargs:
            self._request_case = self._make_case_requester(
                directory=kwargs["directory"]
            )
        elif "bucket" in kwargs:
            self._request_case = self._make_case_requester(bucket=kwargs["bucket"])
        else:
            self._request_case = self._make_case_requester()

        self.all_cases = self._case_generator()

    def _make_case_requester(self, **kwargs):
        def case_request(index=False):
            kwargs["index"] = index
            return Case(**kwargs)

        return case_request

    def _request_generator(self, start, stop):
        case_numbers = range(start, stop + 1)
        for county in self.counties:
            for case_type in self.types:
                for year in self.years:
                    self.exit_year = False
                    for num in case_numbers:
                        case_index = f"{county}-{case_type}-{year}-{num}"
                        yield self._request_case(case_index)
                        if self.exit_year:
                            break

    def _case_generator(self):
        request_attempts = 10
        for case in self._request_generator(self.start, self.stop):
            if case.valid:
                request_attempts = 10
                if case.cmids:
                    for cmid in case.cmids:
                        cmid_index = f"{case.county}-cmid-{case.year}-{cmid}"
                        cmid_case = self._request_case(cmid_index)
                        if cmid_case.valid:
                            if self._passes_filters(cmid_case):
                                yield cmid_case
                elif self._passes_filters(case):
                    yield case
            else:
                if request_attempts > 0:
                    request_attempts -= 1
                else:
                    self.exit_year = True

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.all_cases)

    def _passes_filters(self, case):
        def does_it_pass(filter):
            target, test = filter
            target_value = getattr(case, target)
            if isinstance(test, str):
                return test in target_value
            elif isinstance(test, FunctionType):
                return test(target_value)

        # run the tests
        test_results = map(does_it_pass, self.filters)

        # see if they are all true
        return all(test_results)

    def find(self, **kwargs):
        for kw in kwargs:
            self.filters.append((kw, kwargs[kw]))
        return self
