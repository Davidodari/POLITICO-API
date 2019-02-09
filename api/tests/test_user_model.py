from . import BaseTestCase
from api.v1.models.user_model import UserModel


class PartyModelTest(BaseTestCase):
    def setUp(self):
        self.user = UserModel(
            user={
                "firstname": "David",
                "lastname": "Odari",
                "othername": "Kiribwa",
                "email": "odari@mail.com",
                "phoneNumber": "0717455945",
                "passportUrl": "www.googledrive.com/pics?v=jejfek",
                "password": "12we3e4r"
            })
        self.user_invalid = UserModel(
            user={
                "firstname": "David",
                "lastname": "Od",
                "othername": "Kiribwa",
                "email": "odari@mail.com",
                "phoneNumber": "0717455945",
                "passportUrl": "www.googledrive.com/pics?v=jejfek",
                "password": "12we3e4r"
            })

    def test_user_sign_up(self):
        """
        Test User Model Creates New User
        """
        user_name = self.user.user_sign_up()
        self.assertEqual(user_name, "David")

    def test_user_sign_up_exists(self):
        """
        Test User Model Rejects Duplicate User Sign Up with email
        """
        self.user.user_sign_up()
        user_name = self.user.user_sign_up()
        self.assertEqual(user_name, "User Exists")

    def test_user_sign_up_incorrect_value(self):
        """
        Test User Sign Up fails with insufficient fields
        """
        user_name = self.user_invalid.user_sign_up()
        self.assertEqual(user_name, "Invalid Data Check The Fields")
