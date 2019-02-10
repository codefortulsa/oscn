import oscn


# searhing by name returns a list of CaseList

cases = oscn.find.party(first='Jill',last='Webb')


c = next(cases)

import ipdb; ipdb.set_trace()
print(c.case_index)
print(c.counts)
