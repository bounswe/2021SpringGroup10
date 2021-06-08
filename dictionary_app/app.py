import pymongo
from flask import Flask, render_template, request, redirect, jsonify
import requests

client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
collectiondictionary = db.gokberk


app = Flask(__name__)

if __name__ == '__main__':
    app.run()


@app.route('/dictionary')
def home_dictionary():
    return render_template('search.html')


@app.route("/dictionary-search-synonym/<word>", methods=["GET"])
def synonym_dictionary(word):
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


@app.route("/dictionary-search-definition/<word>", methods=["GET"])
def definition_dictionary(word):
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


@app.route("/dictionary-search", methods=["POST"])
def search_dictionary():
    word = request.form["word"]
    typ = request.form["opr"]
    if typ == "search synonyms":
        x = "http://127.0.0.1:5000/dictionary-search-synonym/" + word
        elements = requests.get(x).json()
    elif typ == "search definitions":
       # elements = definition(word)
        x = "http://127.0.0.1:5000/dictionary-search-definition/" + word
        elements = requests.get(x).json()
    requests.post("http://127.0.0.1:5000/insert-dictionary-history/" + word)
    return render_template("result.html", elements=elements, word=word)


@app.route("/display-dictionary-history", methods=["GET"])
def display_dictionary_hist():
    hist = requests.get("http://127.0.0.1:5000/dictionary-history").json()
    hist2 = {}
    for i, val in enumerate(hist):
        hist2[i+1] = hist[val]
    return render_template("history.html", elements=hist2)


@app.route("/dictionary-history", methods=["GET"])
def get_dictionary_history():
    x = collectiondictionary.find({})
    histdict = {}
    for i, word in enumerate(x):
        histdict[i] = word["word"]
    return histdict


@app.route("/insert-dictionary-history/<word>", methods=["POST", "GET"])
def add_to_dictionary_history(word):
    x = collectiondictionary.insert_one({"word": word})
    return "inserted to history"
