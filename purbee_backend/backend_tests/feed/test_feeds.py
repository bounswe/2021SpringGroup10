import unittest
# from backend_source.app import app
import requests
import uuid

headers = {
    "env": "test"
}

post = {
    "post_type_id": "0b437e0e-d2ae-46d7-8013-947b68ae88ec",
    "post_title": "Example Post Title",
    "post_owner_user_name": "eking",
    "post_entries_dictionary_list": [
        {
            "header": "Event Description",
            "text": "A great hiking event."
        },
        {
            "header": "Event Cost",
            "amount": 28,
            "currency": "TL"
        },
        {
            "header": "Event Location",
            "latitude": 24.8951,
            "longitude": -77.0364,
            "text": "everest mountain."
        },
        {
            "header": "Event Participation"
        },
        {
            "header": "Event Poll",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "can_vote_for_n_many_options": 2
        },
        {
            "header":"date-time",
            "date":"12.03.2021",
            "time":"12.30"
        }
    ]
}



class feedTests(unittest.TestCase):

    def create_post(self):
        result = requests.post("http://0.0.0.0:8080/api/c", json=post)


    def test_user_feed(self):
        self.create_post()
        result = requests.post("http://0.0.0.0:8080/api/user_feed", json={
        "user_name":"berkdddd" },
        headers=headers)
        self.assertEqual(200, result.status_code)
        if result["user_feed_post_list"] != None:
            raise Exception('Wrong output')

    def test_community_feed(self):
        self.create_post()
        result = requests.post("http://0.0.0.0:8080/api/community_feed", json={
        "user_name":"berkdddd",
        "community_id":"10"
        },
        headers=headers)
        self.assertEqual(200, result.status_code)
        if result["community_post_list"] != None:
            raise Exception('Wrong output')

    def test_community_search(self):
        self.create_post()
        result = requests.post("http://0.0.0.0:8080/api/community_search", json={
        "search_text":"exa"
        },
        headers=headers)

        self.assertEqual(200, result.status_code)
        if result["community_names"] is None:
            raise Exception('Wrong output')


if __name__ == '__main__':
    unittest.main()
