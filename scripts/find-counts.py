import sys
import time
import csv

import oscn


counties = ['adair', 'washington']
years = ['2018']

find_descriptions = ['OBSTR', 'RESIST']

def count_test(desc):
    for text in find_descriptions:
        if text in desc:
            return True
    return False

csv_file = open('data/find-counts.csv', "w")
writer = csv.writer(csv_file, delimiter=',')
writer.writerow(["year", "county", "case", "description"])

for county in counties:
    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year)
        count = 0
        for case in case_iter:
            time.sleep(.10)
            sys.stdout.write(case.case_number)
            sys.stdout.flush()

            counts = oscn.parse.counts(case.response.text)
            for count in counts:
                if count_test(count['description']):
                    writer.writerow([year, county, case.case_number, count['description']])
                    sys.stdout.write('*')
                else:
                    sys.stdout.write('.')
            sys.stdout.flush()

csv_file.close()
