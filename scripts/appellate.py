import re
import csv
import sys

import oscn

import logging
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)
logger = logging.getLogger(__name__)

case=oscn.request.Case(number=116264,county='appellate')

case.save(directory='data')

case.save(bucket='oscn-test-data')

# case=oscn.request.Case(type='IN',number=115205,county='appellate', bucket='oscn-test-data')

case=oscn.request.Case(index='appellate-116264', directory='data')

print(case.source)
