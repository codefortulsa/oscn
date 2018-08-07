from os import listdir
from os.path import splitext
from importlib import import_module
from types import FunctionType

# The following code searches for parse functions to allow them to be
# added to objects as properties using the append_parsers function

parse_functions = []

try:
    for py_file in listdir(__path__[0]):
        parse_module = import_module(f'.{splitext(py_file)[0]}', package=__package__)
        for name in dir(parse_module):
            attr = getattr(parse_module, name)
            if isinstance(attr, FunctionType):
                if hasattr(attr,'target'):
                    # replaces 'from .counts import counts'
                    locals()[name] = attr
                    parse_functions.append(attr)
except NameError:
    pass

def make_safe_parser(f):
    def safe_parser(self):
        try:
            return f(self.response.text)
        except:
            return None
    return safe_parser

def make_property(parse_function):
    # return property(lambda self: parse_function(self.response.text))
    return property(make_safe_parser(parse_function))

# this function accepts a class and searches for
# parsers to be added to

def append_parsers(obj):
    for fn in parse_functions:
        if obj.__name__ in fn.target:
            setattr(obj, fn.__name__, make_property(fn))
