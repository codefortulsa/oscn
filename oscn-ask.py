import sys
import time
import oscn.request
from oscn.parse import counts


counties = ['cimarron']
years = ['2018']

for county in counties:
    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year)
        count = 0
        for case in case_iter:
            time.sleep(.10)
            counts = oscn.parse.counts(case['response'].text)
            import ipdb; ipdb.set_trace()
            sys.stdout.write('.')
            sys.stdout.flush()
