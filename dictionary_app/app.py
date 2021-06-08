import pymongo
from flask import Flask, render_template, request, redirect
import requests

client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
collection = db.gokberk
client_id = "82ffff3f23534eedba167129f0ea8e31"
secret = "c8025a5e15754c199d82c249969f484f"


app = Flask(__name__)

if __name__ == '__main__':
    app.run()


@app.route('/')
def home():
    return render_template('search.html')


@app.route("/search-synonym/<word>", methods=["GET"])
def synonym(word):
    url_synonym = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/synonyms"
    headers_synonym = {
        'x-rapidapi-key': "4e9bda707amshaa2a2e7a0c08b4dp1f1264jsn3bb1fb127723",
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }
    response_synonym = requests.request("GET", url_synonym, headers=headers_synonym)
    st = response_synonym.json()
    syns = st["synonyms"]
    synsdict = {}
    for i, val in enumerate(syns):
        synsdict[i+1] = val
    return synsdict


@app.route("/search-definition/<word>", methods=["GET"])
def definition(word):
    url_definition = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/definitions"
    headers_definition = {
        'x-rapidapi-key': "4e9bda707amshaa2a2e7a0c08b4dp1f1264jsn3bb1fb127723",
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }
    response_definition = requests.request("GET", url_definition, headers=headers_definition)
    st = response_definition.json()
    defs = st["definitions"]
    defsdict = {}
    for i, val in enumerate(defs):
        defsdict[i+1]=val["definition"]
    return defsdict


@app.route("/search", methods=["POST"])
def search():
    word = request.form["word"]
    typ = request.form["opr"]
    if typ == "search synonyms":
        elements = synonym(word)
    elif typ == "search definitions":
        elements = definition(word)
    add_to_history(word)
    return render_template("result.html", elements=elements, word=word)


@app.route("/displayhistory", methods=["GET"])
def display_hist():
    hist = get_history()
    hist2 = {}
    for i, val in enumerate(hist):
        hist2[i+1] = hist[i]
    return render_template("history.html", elements=hist2)

@app.route("/history", methods=["GET"])
def get_history():
    x = collection.find({})
    histdict = {}
    for i, word in enumerate(x):
        histdict[i] = word["word"]
    return histdict


@app.route("/inserthistory/<word>", methods=["POST", "GET"])
def add_to_history(word):
    x = collection.insert_one({"word": word})
    return x
