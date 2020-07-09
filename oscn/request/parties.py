
from .. import settings
from ..parse import append_parsers

logger = logging.getLogger("oscn")
logger.setLevel(logging.INFO)

from oscn._meta import party_get


# ?db=tulsa&cn=CF-2020-1&id=12576087

class Party(object):
 
    def __init__(self):
        pass




    def _request(self, attempts_left=settings.MAX_EMPTY_CASES):
        response = requests.post(
                oscn_url, params, headers=self.headers, verify=False
            )
        except ConnectionError:
            if attempts_left > 0:
                return self._request(attempts_left=attempts_left - 1)
            else:
                raise ConnectionError
        if self._valid_response(response):
            self.valid = True
            self.source = f"{response.url}"
            self.text = response.text
            for msg in settings.UNUSED_CASE_MESSAGES:
                if msg in response.text:
                    self.valid = False
                    return
        else:
            self.valid = False


# This next line adds properties to the OSCNrequest as a shortcut
# for parsing.  This allows access to parse results such as:
# name = Case.judge
# or
# counts = Case.counts
append_parsers(Party)