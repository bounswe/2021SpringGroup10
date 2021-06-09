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


    # check market route works
    def test_market(self):
        tester = app.test_client(self)
        response = tester.get("/market")
        stat = response.status_code
        self.assertEqual(stat, 200)

    # check if getCurrencies route works
    def test_getCurrencies(self):
        tester = app.test_client(self)
        response = tester.get("/market/getCurrenciesNames")
        stat = response.status_code
        self.assertEqual(stat, 200)


    # check if history route works
    def test_movies_api(self):
        tester = app.test_client(self)
        response = tester.get("/market/getSearchHistory")
        stat = response.status_code
        self.assertEqual(stat, 200)



def main():
    unittest.main()


if __name__ == "__main__":
    unittest.main()