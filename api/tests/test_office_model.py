from . import BaseTestCase
from api.v1.models.office_model import OfficesModel


class OfficeModelTest(BaseTestCase):

    def setUp(self):
        self.new_office = OfficesModel(office={"name": "Test Office", "type": "Permanent Secretary"})
        self.specific_office = OfficesModel(office_id=1)
        self.specific_office_invalid = OfficesModel(office_id=0)
        self.specific_office_not_exist = OfficesModel(office_id=67)

    def test_creating_government_office(self):
        # Tests Creation Of Office with id
        gen_id = self.new_office.create_government_office()
        assert gen_id == 1

    def test_gets_specific_office(self):
        # Tests Office is returned
        self.new_office.create_government_office()
        office = self.specific_office.get_specific_item()
        assert office['name'] == "Test Office"
        assert office['type'] == "Permanent Secretary"

    def test_gets_specific_party_invalid(self):
        msg = self.specific_office_invalid.get_specific_item()
        assert 'Invalid Id' == msg

    def test_gets_specific_party_not_exist(self):
        self.new_office.create_government_office()
        msg = self.specific_office_not_exist.get_specific_item()
        assert 'Doesnt Exist' == msg

    def test_gets_all_offices_in_list(self):
        self.new_office.create_government_office()
        self.new_office.create_government_office()
        current_list = self.new_office.get_all_items_in_list()
        assert len(current_list) == 2