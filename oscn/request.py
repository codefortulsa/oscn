import requests
import settings

url = settings.OSCN_URL

import warnings
warnings.filterwarnings("ignore")



def is_case_valid(resp):
    if resp.status_code != 200:
        return False
    for msg in settings.INVALID_CASE_MESSAGES:
        if msg in resp.text:
            return False
    return True


class OSCNrequest(object):
    case_number = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
        }

    def __init__(self, type='CF', county='tulsa', year='2018'):
        self.type = type
        self.county = county
        self.year = year

    def case(self):
        return f'{self.type}-{self.year}-{self.case_number}'

    def request_case(self):
        params = {'db': self.county, 'number': self.case()}
        return requests.post(url, params, headers=self.headers, verify=False)


class Case(OSCNrequest):

    def request(self, case_number=1):
        self.case_number = case_number
        response = self.request_case()
        if is_case_valid(response):
            return {'county': self.county, 'case': case, 'response': response}
        else:
            return None


class CaseList(OSCNrequest):
    case_number = 1

    def __iter__(self):
        return self

    def __next__(self):
        case = self.case()
        response = self.request_case()
        if is_case_valid(response):
            self.case_number += 1
            return {'county': self.county, 'case': case, 'response': response}
        else:
            raise StopIteration
