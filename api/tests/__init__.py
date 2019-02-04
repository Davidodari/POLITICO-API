import unittest
# Imports create app function to set testing config
from api import create_app


class BaseTestCase(unittest.TestCase):
    # Base Class for all test files
    def setUp(self):
        # setup flask app instance to testing configuration environment
        self.app = create_app(config='testing')
        self.client = self.app.test_client(self)


if __name__ == '__main__':
    unittest.main()
