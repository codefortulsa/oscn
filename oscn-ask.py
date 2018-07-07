import sys
import time
import oscn.request
import oscn.parse


counties = ['tulsa']
years = ['2018']

for county in counties:
    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year)
        count = 0
        for case in case_iter:
            time.sleep(.10)
            data = oscn.parse.Case(county, case['case'], case['response'].text)
            counts = data.counts()
            import ipdb; ipdb.set_trace()
            sys.stdout.write('.')
            sys.stdout.flush()
