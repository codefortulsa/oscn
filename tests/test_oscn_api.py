import oscn



class TestElasticSearch():

    def setup_class(self):
        changes = {
                "query": {
                    "range": {
                        "lastupdate": {
                            "gte": "now-15m"
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

    def test_get_query(self):
        response = oscn.query(**self.params)
        print(response.text)
        assert response.status_code == 200


class TestGetCaseInfo():

    def setup_class(self):
        self.endpoints =['changes', 'cases', 'events', 'style', 'parties', 'attorneys']

        self.case_params = {'county': 'tulsa', 'cn': 'CF-2020-12'}

    def test_get_dockets(self):
        response = oscn.dockets(**self.case_params)
        print(response.text)
        assert response.status_code == 200
