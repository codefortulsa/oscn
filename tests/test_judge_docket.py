import oscn


class TestGetDocket():

    def setup_class(self):
        self.judge = 1208
        self.start_date = "07/28/2020"
        self.docket = oscn.request.Docket(self.judge, self.start_date)

    def test_get_case_index_list(self):
        all_cases = self.docket.cases
        assert len(all_cases) == 57

    def test_get_case_tables(self):

        all_cases = self.docket.tables

        assert len(all_cases) == 57
