from . import _meta
from . import request
from . import parse
from . import find

from .query.endpoints import events, dockets, counts

from .query.endpoints import style, parties, attorneys

from .query.endpoints import query, updates

from .query.client import client



counties = _meta.courts()
courts = _meta.courts()
judges = _meta.judges()


type = _meta.get_type
types = _meta.all_types()
