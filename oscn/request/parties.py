from .. import settings
from ..parse import append_parsers

logger = logging.getLogger("oscn")
logger.setLevel(logging.INFO)

from oscn._meta import party_get


# ?db=tulsa&cn=CF-2020-1&id=12576087

class Party(object):
 
    def __init__(self):
        pass

    def _request(self):
        party = party_get(self)


# This next line adds properties to the OSCNrequest as a shortcut
# for parsing.  This allows access to parse results such as:
# name = Case.judge
# or
# counts = Case.counts
append_parsers(Party)