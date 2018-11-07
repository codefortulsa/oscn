import re

has_plea = re.compile(r'plea', re.M | re.I)
has_sentance = re.compile(r'sentence', re.M | re.I)

def pleas(case):
    try:
        find_pleas = lambda min: has_plea.search(min['description'])
        return list(filter(find_pleas, case.docket))
    except:
        return []

setattr(pleas, 'target', ['Case'])


def sentences(case):
    try:
        find_sentence = lambda min: has_sentance.search(min['description'])
        return list(filter(find_sentence, case.docket))
    except:
        return []

setattr(sentences, 'target', ['Case'])
