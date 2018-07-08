import sys
import time
import csv

import oscn.request
from oscn.parse import counts


counties = ['cimarron']
years = ['2018']

csv_file = open('data/counts.csv', "w")
writer = csv.writer(csv_file, delimiter=',')
writer.writerow(["year", "county", "case", "description"])

for county in counties:
    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year)
        count = 0
        for case in case_iter:
            time.sleep(.10)
            counts = oscn.parse.counts(case['response'].text)
            for count in counts:
                writer.writerow([year, county, case['case'], count['description']])
            sys.stdout.write('.')
            sys.stdout.flush()

csv_file.close()
