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


class cases(object):
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

# Request URL: https://www.oscn.net/dockets/GetCaseInformation.aspx?db=adair&number=CF-2018-1
# Request Method: GET
# Status Code: 200 OK
# Remote Address: 65.71.189.80:443
# Referrer Policy: no-referrer-when-downgrade
# Cache-Control: no-cache, no-store
# Content-Length: 52111
# Content-Type: text/html; charset=utf-8
# Date: Sat, 30 Jun 2018 16:35:06 GMT
# Expires: -1
# Pragma: no-cache
# Server: Microsoft-IIS/6.0
# X-AspNet-Version: 4.0.30319
# X-Powered-By: ASP.NET
# GET /dockets/GetCaseInformation.aspx?db=adair&number=CF-2018-1 HTTP/1.1
# Host: www.oscn.net
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1
# DNT: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Referer: https://www.oscn.net/dockets/
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-US,en;q=0.9
# Cookie: ASPSESSIONIDQCCBCQTR=IHGFMDIBNIPJGMIEIBBOPMBK; _ga=GA1.2.1540683726.1530217587; _gid=GA1.2.1742424768.1530217587; ASPSESSIONIDQSSDABBT=MAGJGPKCKFPDJGBNAPDAGJNO
# db: adair
# number: CF-2018-1
