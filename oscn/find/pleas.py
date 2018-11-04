import re

find_plea = re.compile(r'plea', re.M | re.I)


def pleas(case):
    minutes_with_pleas = []
    try:
        for min in case.docket:
            if find_plea.search(min['description']):
                minutes_with_pleas.append(min)
        return minutes_with_pleas
    except:
        return []

setattr(pleas, 'target', ['Case'])
