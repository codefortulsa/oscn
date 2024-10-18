import re
from functools import partial

# Precompile regex patterns for efficiency
FILED_PATTERN = re.compile(r"Filed:\s*([\/\d]*)", re.M)
CLOSED_PATTERN = re.compile(r"Closed:\s*([\/\d]*)", re.M)
OFFENSE_PATTERN = re.compile(r"Date.of.Offense:\s*([\/\d]*)", re.M)

def make_date_finder(name, compiled_pattern, default="01/01/1970",target=["Case"]):
    def find_date(text):
        match = compiled_pattern.search(text)
        return match.group(1) if match else default
    
    find_date.__name__ = name
    find_date.target = target 
    return find_date

# Instantiate finders with precompiled patterns
find_filed_date = make_date_finder("filed", FILED_PATTERN)
find_closed_date = make_date_finder("closed", CLOSED_PATTERN)
find_offense_date = make_date_finder("offense", OFFENSE_PATTERN)
