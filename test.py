import sys
import time
import oscn

counties = ['washington', 'cimarron', 'beckham']
#years = ['2017','2018']


#for county in counties:
    #for year in years:
        #sys.stdout.write(f'{county} {year}')
case_iter = oscn.request.CaseList(county=counties, stop=10)
for case in case_iter:
    #sys.stdout.write(case.case_number)
    sys.stdout.flush()
