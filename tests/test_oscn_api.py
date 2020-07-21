import oscn

from datetime import datetime, timedelta


class TestElasticSearch():

    def setup_class(self):
        changes = {
                "query": {
                    "range": {
                        "lastupdate": {
                            "gte": "now-7h"
                        }
                    }
                },
                "size": 10000,
                "_source": [
                    "_id",
                    "lastupdate",
                    "filed",
                    "year",
                    "number",
                    "casetype",
                    "county"
                ]
            }

        self.params = {'q': changes}

    def test_get_client(self):

        pass

    def test_post_query(self):
        response = oscn.query(**self.params)
        print(response.text)
        assert response.status_code == 200

# "start":"2020-07-17T11:59:38-05:00","end":"2020-07-17T12:29:38-05:00",
# "start":"2020-07-17T12:46:24-05:00","end":"2020-07-17T12:46:24-05:00",
    def test_updates(self):
        stop = datetime.now()
        start = stop - timedelta(minutes=60)
        response = oscn.updates(
                start=start,
                end=stop
            )
        print(response.text)
        assert response.status_code == 200

class TestGetCaseInfo():

    def setup_class(self):
        self.endpoints = ['dockets', 'events', 'counts',
                          'style', 'parties', 'attorneys']

        self.case_params = {'county': 'tulsa', 'cn': 'CF-2020-12'}

    def test_get_case_info(self):

        for pt in self.endpoints:
            response = getattr(oscn, pt)(**self.case_params)
            print(response.text)
            assert response.status_code == 200
