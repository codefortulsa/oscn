from os import listdir
from os.path import splitext
from importlib import import_module
from types import FunctionType


# The following code searches for finder functions to allow them to be
# added to objects as properties using the append_parsers function
# it also imports them so they are available from `oscn.find`

find_functions = []

try:
    for py_file in listdir(__path__[0]):
        parse_module = (
            import_module(f'.{splitext(py_file)[0]}', package=__package__)
            )
        for name in dir(parse_module):
            attr = getattr(parse_module, name)
            if isinstance(attr, FunctionType):
                if hasattr(attr, 'target'):
                    # replaces 'from .counts import counts'
                    locals()[name] = attr
                    find_functions.append(attr)
except NameError:
    pass


def make_finder_property(fn):
    def finder_property(self):
        return fn(self)
    return property(finder_property)


# this function accepts a class and searches for
# parsers to be added to
def append_finders(obj):
    for fn in find_functions:
        if obj.__name__ in fn.target:
            setattr(obj, fn.__name__, make_finder_property(fn))
