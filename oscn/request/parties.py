from .. import settings
from ..parse import append_parsers

from oscn._meta import party_get


# ?db=tulsa&cn=CF-2020-1&id=12576087

@append_parsers
class Party(object):

    def __init__(self, party_id):
        self.id = party_id
        self._request()

    def _request(self):
        response = party_get(self.id)
        self.text = response.text
