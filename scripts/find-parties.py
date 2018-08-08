import sys
import time
import csv

import oscn

counties = ['washington', 'cimarron', 'beckham']
years = ['2017','2018']


for county in counties:
    csv_file = open(f'data/{county}-parties.csv', "w")
    # if this breaks, you may need to mkdir data
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["year", "county", "case", "judge", "description","source"])

    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year)
        for case in case_iter:
            sys.stdout.write(case.case_number)
            sys.stdout.flush()
            writer.writerow([year, county, case.case_number, case.judge])
            for party in case.parties:
                writer.writerow([party['name'], party['type']])
                sys.stdout.write('.')
                sys.stdout.flush()

    csv_file.close()
