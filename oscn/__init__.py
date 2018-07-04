import requests
import settings

url = settings.OSCN_URL
county = settings.COUNTY


def is_case_valid(resp):
    if resp.status_code != 200:
        return False
    for msg in settings.INVALID_CASE_MESSAGES:
        if msg in resp.text:
            return False
    return True


class CaseList(object):
    county = "tulsa"
    year = "2018"
    type = "CF"
    case_number = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
        }

    def __init__(self, county, year, *kwargs):
        if county:
            self.county = county
        if year:
            self.year = year

    def __iter__(self):
        return self

    def __next__(self):
        case = f'{self.type}-{self.year}-{self.case_number}'
        params = {'db': self.county, 'number': case}
        response = requests.post(url, params, headers=self.headers, verify=False)
        if is_case_valid(response):
            self.case_number += 1
            return response
        else:
            print(f'Invalid case:{case}')
            raise StopIteration
