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

cases = oscn.request.CaseList(county=counties, year=years)

for case in cases:
    count = 0
    sys.stdout.write(case.oscn_number)
    sys.stdout.flush()
    for count in case.counts:
        if count_test(count['description']):
            writer.writerow([case.year, case.county, case.oscn_number, count['description']])
            sys.stdout.write('*')
        else:
            sys.stdout.write('.')
    sys.stdout.flush()

csv_file.close()
