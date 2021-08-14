from .. import settings
from ..parse import append_parsers

from oscn._meta import docket_get


@append_parsers
class Docket(object):
    def __init__(self, judge_id, start_date):
        self.id = judge_id
        self.start_date = start_date
        self._request()

    def _request(self):
        response = docket_get(self.id, self.start_date)
        self.text = response.text
