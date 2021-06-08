try:
    import sys
    sys.path.insert(1, '../')
    from app import app
    import app as application
    import unittest
    import requests
    import pymongo
    import json

except ImportError as e:
    print("Requirements did not satisfied related to import statements")




class SportEventTest(unittest.TestCase):

    # get test of root route
    def test_get_home(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status = response.status_code
        self.assertEqual(200, status)

    # get test of sportevents route
    def test_get_sportevents(self):
        tester = app.test_client(self)
        response = tester.get("/sportevents")
        status = response.status_code
        self.assertEqual(200, status)


    # get test of sportevents api route
    def test_get_sportevents_api(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1.0/sportevents")
        status = response.status_code
        self.assertEqual(200, status)

    # get test of sportevents with specific type
    def test_get_sportevents_type(self):
        tester = app.test_client(self)
        mock_type = "basketball"
        response = tester.get("/api/v1.0/sportevents/" + mock_type)
        status = response.status_code
        self.assertEqual(200, status)

    # test for adding a event with no description
    def test_api_add_sportevent_with_no_description(self):
        tester = app.test_client(self)
        req = "/api/v1.0/sportevents"
        headers = {'Content-type': 'application/json'}
        event_name = "Test Rugby Event"
        description = "This is a test for rugby event"
        sport_type = "rugby"
        event = {"event_name": event_name, "sport_type": sport_type, "description": description}
        response = tester.post(req, data=json.dumps(event), headers=headers)
        status = response.status_code
        self.assertEqual(201, status)

    # test for adding a event with description
    def test_api_add_sportevent_with_description(self):
        tester = app.test_client(self)
        req = "/api/v1.0/sportevents"
        headers = {'Content-type': 'application/json'}
        event_name = "Test soccer Event"
        description = ""
        sport_type = "soccer"
        event = {"event_name": event_name, "sport_type": sport_type, "description": description}
        response = tester.post(req, data=json.dumps(event), headers=headers)
        status = response.status_code
        self.assertEqual(201, status)


def main():
    unittest.main()


if __name__ == "__main__":
    main()