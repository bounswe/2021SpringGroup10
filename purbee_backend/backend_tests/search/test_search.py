import unittest
# from backend_source.app import app
import requests
import uuid

headers = {
    "env": "test"
}


class searchTests(unittest.TestCase):

    def test_community_search(self):
        result = requests.post("http://0.0.0.0:8080/api/community_search", json={
        "search_text":"exa"
        },
        headers=headers)

        self.assertEqual(200, result.status_code)
        if result["community_names"] is None:
            raise Exception('Wrong output')

    def test_user_search(self):
        result = requests.post("http://0.0.0.0:8080/api/user_search", json={
        "search_text":"ber"
        },
        headers=headers)
        self.assertEqual(200, result.status_code)
        if result["community_names"] is None:
            raise Exception('Wrong output')

    def test_advanced_search(self):
        json = {
        "user_name":"berkdddd",
        "community_id":"10",
        "search_dictionary": {"PlainText": {"search_text":"hiking"},"Location" : {"longitude":-77.0364, "latitude":30, "radius":1000}, "DateTime" : {"starting_date": "10/03/2019" , "ending_date":"15/03/2021", "starting_time": "12:00" , "ending_time":"13:00"},"Participation" : {"min_participation" : 1, "max_participation" : 3}}
        }
        result = requests.post("http://0.0.0.0:8080/api/user_search", json=json
        , headers=headers)
        self.assertEqual(200, result.status_code)
        if "2eb4f558-0bb7-4527-b2dc-312ccbeab368" in result["post_ids"]:
            raise Exception('Wrong output')


if __name__ == '__main__':
    unittest.main()
