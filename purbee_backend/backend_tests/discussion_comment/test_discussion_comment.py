import unittest
import requests


class DiscussionCommentTest(unittest.TestCase):

    def test_first(self):

        result = requests.post("http://0.0.0.0:8080/api/discussion")
        self.assertEqual(201, result.status_code)
        discussion_dict = result.json()["discussion"]
        data = {
            "user_id": "OnurSefa",
            "parent_discussion_id": discussion_dict['id'],
            "text": "comment_text_0"
        }
        result = requests.post("http://0.0.0.0:8080/api/comment", json=data)
        self.assertEqual(201, result.status_code)
        comment_0 = result.json()['comment']

        data['text'] = "comment_text_1"
        result = requests.post("http://0.0.0.0:8080/api/comment", json=data)
        self.assertEqual(201, result.status_code)
        comment_1 = result.json()['comment']

        data['text'] = "comment_text_2"
        data['parent_discussion_id'] = comment_0['discussion_id']
        result = requests.post("http://0.0.0.0:8080/api/comment", json=data)
        self.assertEqual(201, result.status_code)
        comment_2 = result.json()['comment']

        result = requests.get("http://0.0.0.0:8080/api/discussion/{}".format(discussion_dict['id']))
        discussion_dict = result.json()['discussion']
        self.assertTrue(comment_0['id'] in discussion_dict['comment_list'])
        self.assertTrue(comment_1['id'] in discussion_dict['comment_list'])

        result = requests.get("http://0.0.0.0:8080/api/discussion/{}".format(comment_0['discussion_id']))
        discussion_dict = result.json()['discussion']
        self.assertTrue(comment_2['id'] in discussion_dict['comment_list'])

        result = requests.get("http://0.0.0.0:8080/api/discussion/{}".format(comment_1['discussion_id']))
        discussion_dict = result.json()['discussion']
        self.assertFalse(comment_2['id'] in discussion_dict['comment_list'])






if __name__ == '__main__':
    unittest.main()
