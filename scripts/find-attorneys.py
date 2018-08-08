import sys
import time
import csv

import oscn

counties = ['tulsa', 'cimarron']
years = ['2010']


for county in counties:
    csv_file = open(f'data/{county}-attorneys.csv', "w")
    # if this breaks, you may need to mkdir data
    writer = csv.writer(csv_file, delimiter=',')

    for year in years:
        sys.stdout.write(f'{county} {year}')
        case_iter = oscn.request.CaseList(county=county, year=year, start=2168, stop= 2173)
        for case in case_iter:
            sys.stdout.write(case.case_number)
            sys.stdout.flush()
            writer.writerow([year, county, case.case_number])
            for attorney in case.attorneys:
                writer.writerow([attorney])
                sys.stdout.write('.')
                sys.stdout.flush()

    csv_file.close()
