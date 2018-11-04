import oscn

case = oscn.request.Case(county='tulsa', year='2018', number=1)

import ipdb; ipdb.set_trace()

any_pleas = case.pleas
