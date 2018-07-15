import sys
import time
import csv

import oscn.request
from oscn.parse import counts, judge


counties = ['washington', 'cimarron', 'beckham']
years = ['2017','2018']


for county in counties:
    csv_file = open(f'data/{county}-counts.csv', "w")
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["year", "county", "case", "judge", "description","source"])

    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year)
        count = 0
        for case in case_iter:
            # time.sleep(.10)
            sys.stdout.write(case['case'])
            sys.stdout.flush()
            case_judge = oscn.parse.judge(case['response'].text)
            counts = oscn.parse.counts(case['response'].text)
            for count in counts:
                writer.writerow([year, county, case['case'], case_judge, count['description'], case['source']])
                sys.stdout.write('.')
                sys.stdout.flush()

    csv_file.close()
