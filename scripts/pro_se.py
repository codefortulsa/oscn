import oscn
from datetime import datetime
import re

cases = oscn.request.CaseList(county='delaware')

pro_se_re = re.compile(r'waive.*right.*attorney', re.IGNORECASE)

def is_pro_se(case):
    if case.docket:
        for minute in case.docket:
            if pro_se_re.match(minute.description):
                return True
    return False


for case in cases:
    if is_pro_se(case):
        print(case.oscn_number)
    
    # filed = datetime.strptime(case.filed, '%d/%m/%Y')
    # print(filed.date())
