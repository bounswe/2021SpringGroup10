import unittest
# from backend_source.app import app
import requests


class CommunityTest(unittest.TestCase):

    def test_first(self):
        headers = {
            "env": "test"
        }
        data = {
            "admin_id": "123",
            "user_id": "123",
            "community_id": "123",
            "action": "make"
        }
        result = requests.post("http://0.0.0.0:8080/api/community_page/", json=data, headers=headers)
        self.assertEqual(200, result.status_code)

    def test_second(self):
        self.assertFalse(False)


if __name__ == '__main__':
    unittest.main()
