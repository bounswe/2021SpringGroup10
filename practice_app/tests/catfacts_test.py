  
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

    #check start route
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/")
        stat = response.status_code
        self.assertEqual(stat, 200)

    #check catfacts route
    def test_catfacts(self):
        tester = app.test_client(self)
        response = tester.get("/catfacts")
        stat = response.status_code
        self.assertEqual(stat, 200)

    #check catfacts api route
    def test_catfacts_api(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1.0/catfacts")
        stat = response.status_code
        self.assertEqual(stat, 200)

     # test for adding a catfact 
    def test_api_add_catfact(self):
        tester = app.test_client(self)
        req = "/api/v1.0/catfacts"
        headers = {'Content-type': 'application/json'}
        fact = "Cats like people"
        catfact = {"fact": fact}
        response = tester.post(req, data=json.dumps(catfact), headers=headers)
        status = response.status_code
        self.assertEqual(201, status)


def main():
    unittest.main()

    
if __name__ == "__main__":
    unittest.main()