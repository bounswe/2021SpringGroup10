import unittest

from flask import jsonify
import requests

mock_data = {"keywords": "flu", "sources": "nytimes,bbc,guardian"}
mock_news_already_in = {"title": "Erdogan Pulls Turkey From European Treaty on Domestic Violence",
                        "description": "The move is likely to please President Recep Tayyip Erdogan’s conservative followers. He also removed the head of the central bank.",
                        "date": "2021-03-20T12:06:02 00:00",
                        "url": "https://www.nytimes.com/2021/03/20/world/europe/turkey-erdogan-women-violence.html",
                        "source": "The New York Times"}
mock_new_news = {"title": "Who Will Win Record of the Year at the Grammys? Let’s Discuss.",
                        "description": "Beyoncé, Megan Thee Stallion, Billie Eilish, Dua Lipa and more will face off Sunday. In this special “Diary of a Song” episode, critics for The New York Times break down the show’s premier category.",
                        "date": "2021-03-08T18:01:56+00:00",
                        "url": "https://www.nytimes.com/2021/03/08/arts/music/grammys-record-of-the-year.html",
                        "source": "The New York Times"}

API_KEY = "10689593098485c096e61e8dbfc4ac92"

class MyTestCase(unittest.TestCase):

    def testMediaStackAPIAuthorization(self):

        url = "http://api.mediastack.com/v1/news?access_key=%s" % API_KEY
        res = requests.get(url).json()
        self.assertEqual(res.get("error"), None)

    def testMediaStackAPIAGetWithKeywordError(self):

        url = "http://api.mediastack.com/v1/news?access_key=%s" % API_KEY
        keywords = "&keywords=%s" % mock_data["keywords"]
        sources = "&sources=%s" % mock_data["sources"]
        url = url + keywords + sources
        res = requests.get(url).json()
        self.assertEqual(res.get("error"), None)

    def testMediaStackAPIAGetWithKeywordValue(self):

        url = "http://api.mediastack.com/v1/news?access_key=%s" % API_KEY
        keywords = "&keywords=%s" % mock_data["keywords"]
        sources = "&sources=%s" % mock_data["sources"]
        url = url + keywords + sources
        res = requests.get(url).json()
        news = res.get("data")
        news = news[0]
        check = False if ((news["description"] + news["title"] + news["url"]).lower().find(mock_data["keywords"])) == -1 else True
        self.assertTrue(check)


    def testGetFetchWithoutKeywordError(self):
        url = "http://127.0.0.1:5000/news/fetch"
        res = requests.get(url).json()
        self.assertEqual(res.get("error"), None)

    def testGetFetchWithKeywordError(self):
        url = "http://127.0.0.1:5000/news/fetch"
        res = requests.get(url,data=mock_data).json()
        self.assertEqual(res.get("error"), None)

    def testGetFetchWithKeywordValue(self):
        url = "http://127.0.0.1:5000/news/fetch"
        res = requests.get(url,data=mock_data).json()
        news = res.get("News")
        news = news[0]
        check = False if ((news["description"] + news["title"] + news["url"]).lower().find(mock_data["keywords"])) == -1 else True
        self.assertTrue(check)

    def testGetSavedError(self):
        url = "http://127.0.0.1:5000/news/saved"
        res = requests.get(url)
        self.assertNotEqual(res.json(),None)

    def testPostToSavedSomethingAlreadyInDatabase(self):
        url = "http://127.0.0.1:5000/news/saved"
        res = requests.post(url, data=mock_new_news).text
        self.assertEqual(res,"Success")

    def testPostToSavedSomethingAlreadyInDatabase(self):
        url = "http://127.0.0.1:5000/news/saved"
        res = requests.post(url, data=mock_news_already_in).text
        self.assertEqual(res,"Failed")






if __name__ == '__main__':
    unittest.main()
