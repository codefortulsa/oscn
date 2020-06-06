import sys
import time
import csv

import oscn

counties = ["washington", "cimarron", "beckham"]
years = ["2017", "2018"]

cases = oscn.request.CaseList(county=counties, year=years)

for case in cases:
    csv_file = open(f"data/counts.csv", "w")
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(["year", "county", "case", "judge", "description", "source"])
    sys.stdout.write(case.oscn_number)
    sys.stdout.flush()
    for count in case.counts:
        writer.writerow(
            [
                case.year,
                case.county,
                case.oscn_number,
                case.judge,
                count["description"],
                case.source,
            ]
        )
        sys.stdout.write(".")
        sys.stdout.flush()

    csv_file.close()
