import unittest
# from backend_source.app import app
import requests

headers = {
    "env": "test"
}

community = {
    "id": "BOUN",
    "is_private": True,
    "community_creator_id": "OnurSefa"
}


class CommunityTest(unittest.TestCase):

    def test_first(self):

        result = requests.post("http://0.0.0.0:8080/api/community_page/", json=community, headers=headers)
        self.assertEqual(201, result.status_code)

    def test_second(self):
        result = requests.get("http://0.0.0.0:8080/api/community_page/", json=community['id'], headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community_instance']
        self.assertEqual("BOUN", community_dict['id'])
        self.assertEqual("OnurSefa", community_dict['creator_id'])

    def test_third(self):
        data = {
            "user_id": "user_0",
            "community_id": "BOUN"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/subscribe", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertEqual(["user_0"], community_dict['requesters'])

    def test_forth(self):
        data = {
            "community_id": "BOUN",
            "admin_id": "OnurSefa"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/change_privacy", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertEqual([], community_dict['requesters'])
        self.assertFalse(community_dict['is_private'])

    def test_fifth(self):
        result = requests.get("http://0.0.0.0:8080/api/community_page/", json=community['id'], headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community_instance']
        self.assertEqual("BOUN", community_dict['id'])
        self.assertEqual(["user_0"], community_dict['subscriber_list'])

    def test_sixth(self):
        data = {
            "user_id": "user_1",
            "community_id": "BOUN"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/subscribe", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertTrue("user_1" in community_dict['subscriber_list'])

    def test_seventh(self):
        data = {
            "admin_id": "OnurSefa",
            "user_id": "admin_0",
            "community_id": "BOUN",
            "action": "make"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/admin", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertTrue("admin_0" in community_dict['admin_list'])

    def test_eighth(self):
        data = {
            "community_id": "BOUN",
            "admin_id": "admin_0"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/change_privacy", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertTrue(community_dict['is_private'])

    def test_ninth(self):
        data = {
            "user_id": "user_2",
            "community_id": "BOUN"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/subscribe", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertTrue("user_1" in community_dict['requesters'])

    def test_tenth(self):
        data = {
            "admin_id": "admin_0",
            "user_id": "user_2",
            "community_id": "BOUN",
            "action": "accept"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/request", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertFalse("user_2" in community_dict['requesters'])
        self.assertTrue("user_2" in community_dict['subscriber_list'])

    def test_eleventh(self):
        data = {
            "user_id": "user_2",
            "community_id": "BOUN"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/unsubscribe", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertFalse("user_2" in community_dict['subscriber_list'])

    def test_twelfth(self):
        data = {
            "admin_id": "OnurSefa",
            "user_id": "admin_0",
            "community_id": "BOUN",
            "action": "remove"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/admin", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertFalse("admin_0" in community_dict['admin_list'])

    def test_thirteenth(self):
        data = {
            "user_id": "user_2",
            "community_id": "BOUN"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/subscribe", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertTrue("user_1" in community_dict['requesters'])

    def test_fourteenth(self):
        data = {
            "admin_id": "OnurSefa",
            "user_id": "user_2",
            "community_id": "BOUN",
            "action": "reject"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/request", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertFalse("user_2" in community_dict['requesters'])
        self.assertFalse("user_2" in community_dict['subscriber_list'])

    def test_fifteenth(self):
        data = {
            "admin_id": "OnurSefa",
            "user_id": "user_0",
            "community_id": "BOUN",
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/ban", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertTrue("user_0" in community_dict['banned_user_list'])
        self.assertFalse("user_0" in community_dict['subscriber_list'])

    def test_sixteenth(self):
        data = {
            "admin_id": "OnurSefa",
            "user_id": "user_2",
            "community_id": "BOUN",
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/ban", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertTrue("user_2" in community_dict['banned_user_list'])
        self.assertFalse("user_2" in community_dict['subscriber_list'])

    def test_seventeenth(self):
        result = requests.get("http://0.0.0.0:8080/api/community_page/", json=community['id'], headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community_instance']
        self.assertEqual("BOUN", community_dict['id'])
        self.assertTrue("user_1" in community_dict['subscriber_list'])

    def test_eighteenth(self):
        data = {
            "admin_id": "OnurSefa",
            "user_id": "user_0",
            "community_id": "BOUN",
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/unban", json=data, headers=headers)
        self.assertEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertFalse("user_0" in community_dict['banned_user_list'])
        self.assertFalse("user_0" in community_dict['subscriber_list'])

    def test_nineteenth(self):
        data = {
            "admin_id": "OnurSefa",
            "user_id": "user_2",
            "community_id": "BOUN",
            "action": "make"
        }
        result = requests.put("http://0.0.0.0:8080/api/community_page/admin", json=data, headers=headers)
        self.assertNotEqual(200, result.status_code)
        community_dict = result.json()['community']
        self.assertFalse("user_2" in community_dict['admin_list'])






if __name__ == '__main__':
    unittest.main()
