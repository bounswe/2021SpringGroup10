# -*-coding:utf-8-*-
import requests
from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class MyNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=True, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<News %r>' % self.id

    def to_dict(self):
        tmp = {}
        tmp["id"] = self.id
        tmp["title"] = self.title
        tmp["description"] = self.description
        tmp["date"] = self.date
        tmp["url"] = self.url
        tmp["source"] = self.source
        return tmp



@app.route('/saved', methods=['POST', 'GET'])
def saved():
    if request.method == "GET":
        my_news = MyNews.query.order_by(MyNews.id).all()
        return jsonify({"My Pocket": [e.to_dict() for e in my_news]})
    elif request.method == "POST":
        req = request.form.to_dict()
        print(req)
        my_new_news = MyNews(source=req["source"], title=req["title"],
                             description=req["description"],
                             date=req["date"], url=req["url"])
        try:
            db.session.add(my_new_news)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
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
