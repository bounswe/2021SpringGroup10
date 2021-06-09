try:
    import sys
    sys.path.insert(1, '../')
    from app import app
    import app as application
    import unittest
    import requests
    import pymongo
    import json

except Exception as e:
    print("ERROR DETECTED")



class FlaskTest(unittest.TestCase):

    # check home route
    def test_homepage(self):
        tester = app.test_client(self)
        response = tester.get("/")
        stat = response.status_code
        self.assertEqual(stat, 200)

    # check dictionary route
    def test_movies(self):
        tester = app.test_client(self)
        response = tester.get("/dictionary")
        stat = response.status_code
        self.assertEqual(stat, 200)

    # check if synonym route works
    def test_movies_api(self):
        tester = app.test_client(self)
        response = tester.get("/dictionary-search-synonym/test")
        stat = response.status_code
        self.assertEqual(stat, 200)

    # check if definition route works
    def test_movies_api(self):
        tester = app.test_client(self)
        response = tester.get("/dictionary-search-definition/test")
        stat = response.status_code
        self.assertEqual(stat, 200)

    # check if dictionary history route works
    def test_movies_api(self):
        tester = app.test_client(self)
        response = tester.get("/dictionary-history")
        stat = response.status_code
        self.assertEqual(stat, 200)



def main():
    unittest.main()


if __name__ == "__main__":
    unittest.main()