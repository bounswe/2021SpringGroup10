from flask import Flask
import requests
import pandas as pd
from requests.sessions import Request
import numpy as np
from flask import Flask, url_for
from flask import Flask, request, render_template, redirect
import json
import pymongo



app = Flask(__name__)


client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
market_collection = db.berkay

@app.route("/market" ,methods = ["GET","POST"])
def marketHome():
    if request.method == "POST":
        return redirect("/market/getLastDaysForStock",code=307)
    return render_template('home.html')


@app.route("/market/getCurrenciesNames", methods = ["GET"])
def getCurrenciesLastPrice():
    response = requests.get("http://api.marketstack.com/v1/currencies?access_key=10818e5bb1090fefbd86603de2ab9d0c" ).json()
    dict = {}
    for i in response['data']:
        dict[i["code"]] = i["name"]
    return render_template("result.html",result = dict)


@app.route('/market/getLastDaysForStock', methods=["POST"])
def getLastDaysForStock():
    stockName = request.form["Name"]
    Day = request.form["day"]
    url = "http://api.marketstack.com/v1/eod?access_key=10818e5bb1090fefbd86603de2ab9d0c&symbols="+stockName
    response = requests.get(url).json()
    dict = {}
    j=0
    for i in response['data']:
        response = requests.post("http://127.0.0.1:5000/save/{}/{}/{}".format(i["date"][:10],stockName,str(i["close"])+" $"))
        dict[i["date"][:10]] = str(i["close"])+" $"
        j=j+1
        if j== int(Day):
            break
    return render_template('result.html', result=dict)

@app.route('/market/save/<date>/<name>/<price>', methods=["POST"])
def saveLastPrice(date,price,name):
    x = market_collection.insert_one({"name": name, "date": date , "price": price})
    return x


@app.route('/market/getSearchHistory', methods=["GET"])
def getSearchHistory():
    dict2 = {}
    x = market_collection.find({})
    for i,document in enumerate(x):
        dict2[i]= {"name":document["name"],"date":document["date"],"price":document["price"]}
    return dict2

