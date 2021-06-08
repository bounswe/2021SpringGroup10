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
    def test_homepage(self):
        tester = app.test_client(self)
        response = tester.get("/")
        stat = response.status_code
        self.assertEqual(stat, 200)

    #check movies route
    def test_movies(self):
        tester = app.test_client(self)
        response = tester.get("/movies")
        stat = response.status_code
        self.assertEqual(stat, 200)

    #check movies api route
    def test_movies_api(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1.0/movie")
        stat = response.status_code
        self.assertEqual(stat, 200)

     # test for adding a movie 
    def test_api_add_movie(self):
        tester = app.test_client(self)
        req = "/api/v1.0/movie"
        headers = {'Content-type': 'application/json'}
        mmovie = "Eyes Wide Shut"
        movies = {"mmovie": mmovie}
        response = tester.post(req, data=json.dumps(movies), headers=headers)
        status = response.status_code
        self.assertEqual(201, status)


def main():
    unittest.main()


if __name__ == "__main__":
    unittest.main() 