import oscn


class TestPartyProperties:
    def setup_class(self):
        case = oscn.request.Case("tulsa-CF-2020-1")
        defendant_id = case.parties[0]["id"]
        defendant = oscn.request.Party(defendant_id)
        self.defendant = defendant

    def test_get_party_dob(self):
        this_profile = self.defendant.profile
        dob = this_profile["Birth Month and Year"]
        assert dob == "05/1991"

    def test_get_party_name(self):
        name = self.defendant.name
        assert name == "JONES, STUART CHANCE"

    def test_get_party_alias(self):
        alias = self.defendant.alias
        assert alias == "JONES, STEWART CHANCE"

    def test_get_party_birthmonth(self):
        mob = self.defendant.birth_month
        assert mob == "05/1991"

    def test_party_addreseses(self):
        party_addresses = self.defendant.addresses
        assert len(party_addresses) == 5
        assert party_addresses[2]["Address"] == "TULSA, Oklahoma 74115"

    def test_party_source(self):
        party_source = self.defendant.source
        assert (
            party_source
            == "https://www.oscn.net/dockets/GetPartyRecord.aspx?db=oklahoma&id=12576087"
        )

# SKIPPING TO GET FIXES TO EVENTS AND PARTIES PUBLSIHED
# class TestDifferentDB:
#     def setup_class(self):
#         case = oscn.request.Case("kingfisher-CF-2018-16")
#         defendant_id = case.parties[0]["id"]
#         defendant = oscn.request.Party(defendant_id, case.county)
#         self.defendant = defendant

#     def test_party_db(self):
#         party_name = self.defendant.name
#         assert party_name == "HUDSON, PHILLIP JOSEPH"
