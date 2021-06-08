# -*-coding:utf-8-*-
import pymongo as pymongo
import requests
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
news_collection = db.news



@app.route('/saved', methods=['POST', 'GET'])
def saved():
    if request.method == "GET":
        my_news = news_collection.find({})
        lst = []
        for e in my_news:
            tmp = {"source": e["source"],
            "title": e["title"],
            "description": e["description"],
            "date": e["date"],
            "url": e["url"]}
            lst.append(tmp)
            
        return jsonify({"My Pocket": lst})

    elif request.method == "POST":
        req = request.values.to_dict()
        print(req)
        if not req:
            req = request.json

        my_new_news = {"_id":req["title"],
        "source":req["source"],
        "title":req["title"],
        "description":req["description"],
        "date":req["date"],
        "url":req["url"]}

        try:
            news_collection.insert_one(my_new_news)
        except Exception as e:
            return "Failed"
        return "Success"


@app.route('/fetch', methods=['GET'])
def fetch():
    s_keyword = request.form.get("keywords")
    # IndexedNews.query.delete()
    API_KEY = "10689593098485c096e61e8dbfc4ac92"
    url = "http://api.mediastack.com/v1/news?access_key=%s" % API_KEY
    limit = "&limit=100"
    sources = "&sources=%s" % "nytimes,bbc,guardian"
    if s_keyword:
        keywords = "&keywords=%s" % s_keyword
    else:
        keywords = ""
    languages = "&lanuages=en,-ar,-de,-es,-fr,-he,-it,-nl,-no,-pt,-ru,-se,-zh"
    url = url + keywords + limit + languages + sources
    response = requests.get(url)
    dict = response.json()
    new_dict = {}
    news_list = []
    for news in dict["data"]:
        news["description"] = "No Description" if not news["description"] else news["description"]
        tmp_dict = {"title": news["title"],
                    "description": news["description"],
                    "date": news["published_at"],
                    "url": news["url"],
                    "source": news["source"]}
        news_list.append(tmp_dict)

    new_dict["News"] = news_list
    return jsonify(new_dict)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        res = requests.get("http://127.0.0.1:5000/fetch", data={'keywords': request.form['keywords']}).json()
        return render_template('index.html', news=res["News"])

    if request.method == 'GET':
        response = requests.get("http://127.0.0.1:5000/fetch")
        resp = response.json()
        return render_template('index.html', news=resp["News"])


@app.route('/pocket', methods=['GET', 'POST'])
def pocket():
    if request.method == 'POST':
        params = {'source': request.form['source'],
                  'title': request.form['title'],
                  'description': request.form['description'],
                  'date': request.form['date'],
                  'url': request.form['url']}
        res = requests.post("http://127.0.0.1:5000/saved",data= params)
        return redirect("/pocket")

    elif request.method == 'GET':
        response = requests.get("http://127.0.0.1:5000/saved")
        resp = response.json()
        return render_template('pocket.html', news=resp["My Pocket"])


if __name__ == '__main__':
    app.run(debug=True)
