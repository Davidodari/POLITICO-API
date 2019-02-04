from . import BaseTestCase
import json


class OfficeEndpointsTestCase(BaseTestCase):

    def test_create_office(self):
        """Tests POST Http method request on /offices endpoint"""
        # Post, uses office specification model
        response = self.client.post('/offices',
                                    json={
                                        'id': 1234567890,
                                        'type': 'Senior',
                                        'name': 'Permanent Secretary'
                                    })
        # Data section returned as per response specification
        expected_response_data = {
            'data': [{
                'id': 1234567890,
                'type': 'Senior',
                'name': 'Permanent Secretary'
            }]
        }
        # makes JSON Object a string
        expected_data_json = json.dumps(expected_response_data)
        # Assert - (expected,actual)
        self.assertEqual(201, response.status, "Should Return a 201 HTTP Status Code Response:Created Successfully")
        self.assertEqual(expected_data_json, str(response.data))

    def test_create_office_bad_request(self):
        """Tests malformed POST Http method request on /offices endpoint"""
        response = self.client.post('/offices',
                                    json={
                                        'id': 1234567890,
                                        # Missing type key
                                        'name': 'Permanent Secretary'
                                    })
        self.assertEqual(400, response.status, "Should Return a 400 HTTP Status Code Response:Bad Request")
        # Should return error message
        self.assertIn("Bad Request", str(response.error), "Should return bad request response")

    def test_view_all_offices(self):
        """Tests GET Http method request on /offices endpoint"""
        # Post, create an office first
        office = {
            'id': 1234567890,
            'type': 'Senior',
            'name': 'Permanent Secretary'
        }
        self.client.post('/offices', json=office)
        # Retrieve the office
        response = self.client.get('/offices')
        # Assert - (expected,actual)
        self.assertEqual(200, response.status, "Should Return a 200 HTTP Status Code Response:Success")
        # Converts to string
        self.assertIn(json.dumps({'data': [office]}), str(response.data))

    def test_view_all_offices_bad_request(self):
        """Tests malformed GET Http method request on /office endpoint"""
        response = self.client.get('/ofices')
        self.assertEqual(404, response.status, "Should Return a 404 HTTP Status Code Response:Not Found")
        # Should return error message
        self.assertIn("Not Found", str(response.error), "Should return resource not found response")

    def test_view_specific_office(self):
        """Tests GET Http method request on /office/{:id} endpoint"""
        # Post, add an office
        office = {
            'id': 1234567890,
            'type': 'Senior',
            'name': 'Permanent Secretary'
        }
        self.client.post('/offices',
                         json=office)

        # Get data for specific office
        response = self.client.get('/offices/{0}'.format(office['id']))
        self.assertEqual(200, response.status, "Should Return a 200 HTTP Status Code:Success")
        # Returns Dict as string and compares if its in response
        self.assertIn(json.dumps({'data': [office]}), str(response.data))

    def test_view_specific_office_not_found(self):
        """Tests malformed GET Http method request on /office/{:id} endpoint"""
        response = self.client.get('/offices/45789')
        self.assertEqual(404, response.status, "Should Return a 404 HTTP Status Code Response:Not Found")
        # Should return error message
        self.assertIn("Not Found", str(response.error), "Should return resource not found response")
