from . import BaseTestCase
import json


class OfficeEndpointsTestCase(BaseTestCase):
    def test_office_creation_success(self):
        """
        Tests Office Created Successfully
        """
        response = self.client.post('api/v2/offices', data=json.dumps({
            "type": "Health",
            "name": "Senior Medical Staff"
        }), headers=self.generate_token())
        self.assertEqual(response.status_code, 201, "Office Creation should be Successful")
        self.assertEqual('Senior Medical Staff', response.json['data'][0]['name'])

    def test_office_created_exists(self):
        """ Tests No office was Duplicated """
        data = {
            "type": "Health",
            "name": "Senior Medical Staff"
        }
        self.client.post('api/v2/offices', data=json.dumps(data), headers=self.generate_token())
        response = self.client.post('api/v2/offices', data=json.dumps(data), headers=self.generate_token())
        self.assertEqual(response.status_code, 409, "Office Should Already Exists")
        self.assertEqual('Office Already Exists', response.json['error'])

    def test_created_office_with_invalid_data(self):
        """
        Tests Office with invalid data
        """
        response = self.client.post('api/v2/offices', data=json.dumps({
            "name": "r",
            "type": "yu"
        }), headers=self.generate_token())
        self.assertEqual(response.status_code, 400, "Should be Parsing Invalid Data ,Bad Request")
        self.assertIn('Check Input Values', response.json['error'])

    def test_create_office_with_missing_data(self):
        """
        Tests create office with missing data
        """
        response = self.client.post('api/v2/offices', data=json.dumps({
            "name": "Attorney General"
        }), headers=self.generate_token())
        self.assertEqual(response.status_code, 400, "Should be Parsing Invalid Data ,Bad Request")
        self.assertIn('Missing Key value', response.json['error'])

    def test_get_all_offices_empty_set(self):
        """Tests that the offices in the db are retrived as empty list if none"""
        response = self.client.get('api/v2/offices', headers=self.generate_token())
        self.assertEqual(response.status_code, 200, "Should be getting all offices")
        self.assertEqual(0, len(response.json['data']))

    def test_get_all_offices_success(self):
        """Tests that all offices are retrieved """
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Goverment Official",
            "type": "Patrol"
        }), headers=self.generate_token())
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Government Steward",
            "type": "Patrol"
        }), headers=self.generate_token())
        response = self.client.get('api/v2/offices', headers=self.generate_token())
        self.assertEqual(response.status_code, 200, "Should be getting all offices")
        self.assertEqual(2, len(response.json['data']))

    def test_office_edited_successfully(self):
        """"Tests that offices are edited successfully"""
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Government Steward",
            "type": "Patrol"
        }), headers=self.generate_token())
        response = self.client.patch('api/v2/offices/{}/name'.format(1), data=json.dumps({
            "name": "President"
        }), headers=self.generate_token())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated successfully', response.json['message'])

    def test_office_edited_unsuccessful_missing_key(self):
        response = self.client.patch('api/v2/offices/{}/name'.format(1), data=json.dumps({
        }), headers=self.generate_token())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing Key value', response.json['error'])

    def test_office_edited_exists(self):
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Government Steward",
            "type": "Patrol"
        }), headers=self.generate_token())
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Government This",
            "type": "Patroler"
        }), headers=self.generate_token())
        response = self.client.patch('api/v2/offices/{}/name'.format(1), data=json.dumps({
            "name": "Government This"
        }), headers=self.generate_token())
        self.assertEqual(response.status_code, 409)
        self.assertIn('Office with similar name exists', response.json['error'])

    def test_office_edited_data_invalid(self):
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Government Steward",
            "type": "Patrol"
        }), headers=self.generate_token())
        response = self.client.patch('api/v2/offices/{}/name'.format(1), data=json.dumps({
            "name": "G"
        }), headers=self.generate_token())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Data ,Check id or data being updated', response.json['error'])

    def test_specific_office_success(self):
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Government Steward",
            "type": "Patrol"
        }), headers=self.generate_token())
        response = self.client.get("api/v2/offices/1", headers=self.generate_token())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Government Steward', response.json['data'][0]['office_name'])

    def test_get_non_existing_office(self):
        response = self.client.get("api/v2/offices/1", headers=self.generate_token())
        self.assertEqual(response.status_code, 404)
        self.assertIn('Data Not Found', response.json['error'])

    def test_get_office_with_invalid_id(self):
        response = self.client.get("api/v2/offices/---", headers=self.generate_token())
        self.assertEqual(response.status_code, 404)
        self.assertIn('Data Not Found', response.json['error'])

    def test_delete_office_success(self):
        self.client.post('api/v2/offices', data=json.dumps({
            "name": "Government Steward",
            "type": "Patrol"
        }), headers=self.generate_token())
        response = self.client.delete("api/v2/offices/1", headers=self.generate_token())
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Government Steward Deleted', response.json['message'])

    def test_delete_item_fail(self):
        response = self.client.delete("api/v2/offices/1", headers=self.generate_token())
        self.assertEqual(response.status_code, 404)
        self.assertEqual('Data Not Found', response.json['error'])
