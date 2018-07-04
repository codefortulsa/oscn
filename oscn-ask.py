import sys
import time
from oscn import *

counties = ['tulsa']
years = ['2018', '2017']


start = time.clock()

for county in counties:
    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year)
        count = 0
        for case in case_iter:
            time.sleep(.10)
            data = oscn.parse.Case(county, case['number'], case['response'].text)
            import ipdb; ipdb.set_trace()

            sys.stdout.write('.')
            sys.stdout.flush()
