from . import BaseTestCase
import json


class PartiesEndpointsTestCase(BaseTestCase):
    def test_create_political_party(self):
        """Tests POST Http method request on /parties endpoint"""
        # Post, uses party specification model
        response = self.client.post(path='/api/v1/parties', data=json.dumps(self.party))
        expected_data_json = {
            'data': [{
                'id': 1,
                'name': 'Pinnacle Party'
            }],
            "status": 201
        }
        assert response.status_code == 201, "Should Return a 201 HTTP Status Code Response"
        assert expected_data_json == response.json

    def test_create_political_party_bad_request(self):
        """Tests malformed POST Http method request on /parties endpoint"""
        response = self.client.post('api/v1/parties',
                                    json={
                                        # Missing hq address and logo url
                                        'name': 'Pinnacle Party'
                                    })
        assert response.status_code == 400, "Should Return a 400 HTTP Status Code Response:Bad Request"
        # Should return error message
        assert "BAD REQUEST" in str(response.json), "Should return bad request response"

    def test_edit_political_party(self):
        """Tests PATCH Http method request on /parties/{:id}/name endpoint"""
        # Save Post First
        self.client.post('api/v1/parties', data=json.dumps(self.party))
        edit_request_json = {
            "name": "Dynamo Party"
        }
        # Update Name
        response = self.client.patch('api/v1/parties/{}/name'.format(1),
                                     data=json.dumps(edit_request_json), content_type='application/json')
        assert response.status_code == 200, "Should Return a 200 HTTP Status Code Response:Updated"
        assert "Dynamo Party" == response.json['data'][0]['name']

    def test_edit_political_party_not_found(self):
        """Tests malformed PATCH Http method request on /parties/{:id}/name endpoint"""
        response = self.client.patch('/parties/{}/name'.format(1))
        assert response.status_code == 404, "Should Return a 404 HTTP Status Code Response:Not Found"
        # Should return error message
        assert self.error_not_found == response.json, "Should return not found response"

    def test_delete_political_party(self):
        """Tests DELETE Http method request on /parties/{:id} endpoint"""
        # Save Post First
        # self.client.post('/parties', json=self.party)
        # # Delete Post
        # response = self.client.delete('/parties/{0}'.format(self.party['id']))
        # assert 204 == response.status, "Should Return a 204 HTTP Status Code Response:Deleted"
        # assert "Deleted" in str(response.data)
        pass

    def test_delete_political_party_not_found(self):
        """"Tests malformed DELETE Http method request on /parties/{:id} endpoint"""
        # response = self.client.delete('/parties/0')
        # assert 404 == response.status, "Should Return a 404 HTTP Status Code Response:Not Found"
        # # Should return error message
        # assert "Not Found" in str(response.error), "Should return resource not found response"
        pass

    def test_view_political_party(self):
        """Tests GET Http method request on /parties/{:id} endpoint"""
        # Create Party First
        self.client.post('api/v1/parties', data=json.dumps(self.party))
        # Get data for specific party
        response = self.client.get('api/v1/parties/{0}'.format(1))
        expected_response = {
            "id": 1,
            "name": "Pinnacle Party",
            "hqAddress": "Nairobi,Kenya 00100",
            "logoUrl": "https://www.some.url.co.ke"
        }
        assert response.status_code == 200, "Should Return a 200 HTTP Status Code:Success"
        # Returns Dict as string and compares if its in response
        assert expected_response == response.json['data'][0]

    def test_view_political_party_invalid_id(self):
        """Tests malformed GET Http method request on /parties/{:id} endpoint"""
        response = self.client.get('api/v1/parties/{}'.format(0))
        assert response.status_code == 404, "Should Return a 404 HTTP Status Code Response:Not Found"
        # Should return error message
        assert self.invalid_id_json == response.json, "Should return resource not found response"

    def test_view_specific_office_not_found(self):
        """Tests malformed GET Http method request on /office/{:id} endpoint"""
        response = self.client.get('api/v1/partiess/{}'.format(0))
        assert 404 == response.status_code, "Should Return a 404 HTTP Status Code Response:Not Found"
        # Should return error message
        assert self.error_not_found == response.json, "Should return resource not found response"

    def test_view_all_political_parties(self):
        """Tests GET Http method request on /parties/ endpoint"""
        # Post, create a political party
        self.client.post('api/v1/parties', data=json.dumps(self.party))
        # Retrieve the office
        response = self.client.get('api/v1/parties')
        expected_response_json = {
            "data": [{
                "id": 1,
                "name": "Pinnacle Party",
                "hqAddress": "Nairobi,Kenya 00100",
                "logoUrl": "https://www.some.url.co.ke"
            }],
            "status": 200
        }
        # Assert - (expected,actual)
        assert 200 == response.status_code, "Should Return a 200 HTTP Status Code Response:Success"
        # Converts to string
        assert expected_response_json == response.json

    def test_view_all_political_parties_empty_list(self):
        """Tests malformed GET Http method request on /parties/ endpoint"""
        response = self.client.get('api/v1/parties')
        assert response.status_code == 200, "Should Return a 200 HTTP Status Code Response:Success"
        expected_response_json = {
            "data": [],
            "status": 200
        }
        # Should return error message
        assert expected_response_json == response.json, "Should return [] empty list"

    def test_view_all_political_parties_wrong_path(self):
        """Tests malformed GET Http method request on /parties/ endpoint"""
        response = self.client.get('api/v1/partis')
        assert response.status_code == 404, "Should Return a 404 HTTP Status Code Response:Resource Not Found"
        # Should return error message
        assert self.error_not_found == response.json, "Should return not found Response"
