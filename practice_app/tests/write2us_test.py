import unittest
import os
import sys
sys.path.insert(1, '../')
from app import app
import app as application
import json

class Write2UsTest(unittest.TestCase):

    def setUp(self):
        self.mock_data_1 = [
            {"fname": "ali", "lname": "veli", "message": "good job! looking good already."},
            {"fname": "ayşe", "lname": "fatma", "message": "hey guys why did you kick me out of the group??"},
            {"fname": "murat", "lname": "sürat", "message": "I was wondering if you guys need help with anything."}
        ]
        self.mock_data_2 = [
            "60c067ae16df34f5c5049c57",
            "60bfc8a20c1b17c7c4ce196c",
            "60bfc8680e14dd25d0e5e802"
        ]

    def test_write2channel(self):
        tester = app.test_client(self)
        for data in self.mock_data_1:
            return_value = tester.post(f'/write2channel/{data["fname"]}/{data["lname"]}/{data["message"]}')
            self.assertEqual(return_value.status, '200 OK')
            response_data = json.loads(return_value.data)
            self.assertEqual(len(response_data['id']), 24)
    
    def test_check_replies(self):
        tester = app.test_client(self)
        for data in self.mock_data_2:
            return_value = tester.get(f'/slack-replies/{data}')
            self.assertEqual(return_value.status, '200 OK')
            response_data = json.loads(return_value.data)
            self.assertEqual(type(response_data['replies']), list)

if __name__ == '__main__':
    unittest.main()
