from . import BaseTestCase
import json


class OfficeEndpointsTestCase(BaseTestCase):

    def test_create_office(self):
        """Tests POST Http method request on /offices endpoint"""
        # Post, uses office specification model
        response = self.client.post('/offices', json=self.office)
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
        assert 201 == response.status, "Should Return a 201 HTTP Status Code Response:Created Successfully"
        assert expected_data_json == str(response.data)

    def test_create_office_bad_request(self):
        """Tests malformed POST Http method request on /offices endpoint"""
        response = self.client.post('/offices',
                                    json={
                                        'id': 1234567890,
                                        # Missing type key
                                        'name': 'Permanent Secretary'
                                    })
        assert 400 == response.status, "Should Return a 400 HTTP Status Code Response:Bad Request"
        # Should return error message
        assert "Bad Request" in str(response.error), "Should return bad request response"

    def test_view_all_offices(self):
        """Tests GET Http method request on /offices endpoint"""
        # Post, create an office first
        self.client.post('/offices', json=self.office)
        # Retrieve the office
        response = self.client.get('/offices')
        # Assert - (expected,actual)
        assert 200 == response.status, "Should Return a 200 HTTP Status Code Response:Success"
        # Converts to string
        assert json.dumps({'data': [self.office]}) in str(response.data)

    def test_view_all_offices_bad_request(self):
        """Tests malformed GET Http method request on /office endpoint"""
        response = self.client.get('/ofices')
        assert 404 == response.status, "Should Return a 404 HTTP Status Code Response:Not Found"
        # Should return error message
        assert "Not Found" in str(response.error), "Should return resource not found response"

    def test_view_specific_office(self):
        """Tests GET Http method request on /office/{:id} endpoint"""
        # Post, add an office
        self.client.post('/offices', json=self.office)
        # Get data for specific office
        response = self.client.get('/offices/{0}'.format(self.office['id']))
        assert 200 == response.status, "Should Return a 200 HTTP Status Code:Success"
        # Returns Dict as string and compares if its in response
        assert json.dumps({'data': [self.office]}) in str(response.data)

    def test_view_specific_office_not_found(self):
        """Tests malformed GET Http method request on /office/{:id} endpoint"""
        response = self.client.get('/offices/45789')
        assert 404 == response.status, "Should Return a 404 HTTP Status Code Response:Not Found"
        # Should return error message
        assert "Not Found" in str(response.error), "Should return resource not found response"