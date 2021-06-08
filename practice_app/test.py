try:
    from app import app
    import unittest
    import requests
    import pymongo

except Exception as e:
    print("Some error have occured")

client = pymongo.MongoClient("mongodb+srv://baseuser:baseuser@cluster0.cjzn1.mongodb.net/352api?"
                             "retryWrites=true&w=majority")
db = client["352api"]

class FlaskTest(unittest.TestCase):

    #check start route
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/weather")
        stat = response.status_code
        self.assertEqual(stat, 200)

    #check get request of wheatherget route
    def test_weatherget(self):
        tester = app.test_client(self)
        response = tester.get("/weatherget")
        stat = response.status_code
        self.assertEqual(stat, 200)

    # check get request of wheatherpost route
    def test_weatherpost(self):
        tester = app.test_client(self)
        response = tester.post("/weatherpost/ISTANBUL")
        stat = response.status_code
        self.assertEqual(stat, 200)




if __name__ == "__main__":
    unittest.main()