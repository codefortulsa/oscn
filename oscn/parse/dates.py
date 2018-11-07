import re
from datetime import datetime


def make_pattern_finder(pattern):
    find = re.compile(pattern, re.M)

    def find_pattern(oscn_html):
        search = find.search(oscn_html)
        try:
            return search.group(1)
        except AttributeError:
            return ''

    return find_pattern

find_filed = make_pattern_finder(r'Filed:\s*([\/\d]*)')
find_filed.__name__ = 'filed'
setattr(find_filed, 'target', ['Case'])

find_closed = make_pattern_finder(r'Closed:\s*([\/\d]*)')
find_closed.__name__ = 'closed'
setattr(find_closed, 'target', ['Case'])

find_offense = make_pattern_finder(r'Date.of.Offense:\s*([\/\d]*)')
find_offense.__name__ = 'offense'
setattr(find_offense, 'target', ['Case'])
