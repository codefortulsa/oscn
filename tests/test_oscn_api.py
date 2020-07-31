import oscn


class TestGetCaseInfo:
    def setup_class(self):

        self.endpoints = ["style"]
        self.list_endpoints = ["docket", "events", "counts", "parties", "attorneys"]

        self.case_params = {"county": "tulsa", "cn": "CF-2020-12"}

        self.case_index = {"index": "tulsa-CF-2020-12"}

    def test_get_case_dict(self):
        for pt in self.endpoints:
            response = getattr(oscn.json, pt)(**self.case_params)
            print(f"{pt}: {response}")
            assert type(response) == dict

    def test_get_case_lists(self):
        for pt in self.list_endpoints:
            response = getattr(oscn.json, pt)(**self.case_params)
            print(f"{pt}: {response}")
            assert type(response) == list

    def test_use_case_index(self):
        for pt in self.list_endpoints:
            response = getattr(oscn.json, pt)(**self.case_index)
            print(f"{pt}: {response}")
            assert type(response) == list
