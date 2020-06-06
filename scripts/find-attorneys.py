import sys
import time
import csv

import oscn

counties = ["tulsa", "cimarron", "adair", "delaware"]
years = ["2010"]


for county in counties:
    csv_file = open(f"data/{county}-attorneys.csv", "w")
    # if this breaks, you may need to mkdir data
    writer = csv.writer(csv_file, delimiter=",")

    for year in years:
        sys.stdout.write(f"{county} {year}")
        case_iter = oscn.request.CaseList(county=county, year=year, stop=25)
        for case in case_iter:
            sys.stdout.write(case.oscn_number)
            sys.stdout.flush()
            writer.writerow([year, county, case.oscn_number])
            writer.writerow(case.attorneys)
            sys.stdout.write(".")
            sys.stdout.flush()

    csv_file.close()
