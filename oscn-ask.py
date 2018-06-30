import oscn_search as oscn
import sys

cases = oscn.cases(county='adair', year="2018")

# import warnings
# warnings.filterwarnings("ignore")

for case in cases:
    sys.stdout.write('.')
