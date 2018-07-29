from importlib import import_module
from types import FunctionType

# these import statements expose parsers for use as oscn.parse.{function}
from .counts import counts
from .parties import parties
from .judge import judge
from .docket import docket
from .events import events


# The following code searches for parse function to allow them to be
# added to objects as properties using the append_parsers function

parse_modules = ['counts',
                 'dates',
                 'docket',
                 'events',
                 'judge',
                 'parties',
                 ]

parse_functions = []
for py in parse_modules:
    parse_module = import_module(f'.{py}', package='oscn.parse')
    for name in dir(parse_module):
        attr = getattr(parse_module, name)
        if isinstance(attr, FunctionType):
            if hasattr(attr,'target'):
                parse_functions.append(attr)


def make_property(parse_function):
    return property(lambda self: parse_function(self.response.text))

# this function accepts a class and searches for
# parsers to be added to it
def append_parsers(obj):
    for fn in parse_functions:
        if obj.__name__ in fn.target:
            setattr(obj, fn.__name__, make_property(fn))
