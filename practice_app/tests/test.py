try:
    import sys
    sys.path.insert(1, '../')
    from app import app
    import app as application
    import unittest
    import requests
    import pymongo

except ImportError as e:
    print("Requirements did not satisfied related to import statements")


mock_data = {
    "name": "mock_user",
    "jokes": [
        {
            "set_up": "set_up_value_one",
            "punch_line": "punch_line_value_one"
        },
        {
            "set_up": "set_up_value_two",
            "punch_line": "punch_line_value_two"
        }
    ]
}

will_deleted_mock_data = {
    "name": "will_deleted_mock_data",
    "jokes": [

    ]
}

will_appended_joke = {
    "name": "will_deleted_mock_data",
    "set_up": "set_up_value_three",
    "punch_line": "punch_line_value_three"
}


def equality_check(datum_one, datum_two):
    if datum_one["name"] != datum_two["name"]:
        return False
    for d_one, d_two in zip(datum_one["jokes"], datum_two["jokes"]):
        if d_one != d_two:
            return False

    return True


class JokeTest(unittest.TestCase):

    # get test of home route
    def test_get_home(self):
        tester = app.test_client(self)
        response = tester.get("/joke/")
        status = response.status_code
        self.assertEqual(200, status)

    # get test of choice route
    def test_get_choice(self):
        tester = app.test_client(self)
        response = tester.get("/joke/choice")
        status = response.status_code
        self.assertEqual(200, status)

    # get test of make a joke route
    def test_get_make(self):
        tester = app.test_client(self)
        application.joke_user[0] = True
        application.joke_user[1] = "Onur"
        response = tester.get("/joke/user/make")
        status = response.status_code
        self.assertEqual(200, status)

    # get test of show jokes route
    def test_get_show(self):
        tester = app.test_client(self)
        application.joke_user[0] = True
        application.joke_user[1] = "Onur"
        response = tester.get("/joke/user/show")
        status = response.status_code
        self.assertEqual(200, status)

    # redirect property oh unrelated url
    def test_get_unrelated_url(self):
        tester = app.test_client(self)
        response = tester.get("/joke/user/unrelated")
        status = response.status_code
        self.assertEqual(302, status)

    # test for getting user information
    def test_api_get_user_info(self):
        tester = app.test_client(self)
        response = tester.get("/joke/get_user/{}".format(mock_data["name"]))
        status = response.status_code
        self.assertEqual(200, status)
        self.assertFalse(not equality_check(response.json, mock_data))

    # test for adding a user
    def test_api_add_user(self):
        tester = app.test_client(self)
        response = tester.post("/joke/add_user/{}".format(will_deleted_mock_data['name']))
        status = response.status_code
        self.assertEqual(200, status)

    # test for updating a user
    def test_api_update_user(self):
        tester = app.test_client(self)
        set_up = will_appended_joke["set_up"]
        punch_line = will_appended_joke["punch_line"]
        response = tester.put('/joke/add_to_list/{}/{}/{}'.format("update_user", set_up, punch_line))
        status = response.status_code
        self.assertEqual(200, status)

    # test for deleting a user
    def test_api_delete_user(self):
        tester = app.test_client(self)
        name = will_deleted_mock_data["name"]
        response = tester.delete("/joke/delete_user/{}".format(name))
        status = response.status_code
        self.assertEqual(200, status)
        self.assertFalse(response.json['deleted_count'] > 1)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
