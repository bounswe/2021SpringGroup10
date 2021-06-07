from flask import Flask, jsonify, request, render_template
import requests
import pymongo
import datetime


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://baseuser:baseuser@cluster0.cjzn1.mongodb.net/352api?"
                             "retryWrites=true&w=majority")
db = client["352api"]


@app.route('/weatherget', methods=['GET'])
def weatherget():
    #response = db.weather.find().sort("time", -1)

    for result in response:
        temp = result.pop('_id')
        return render_template('weatherGet.html', data=result)
        break


@app.route('/weatherpost', methods=['POST'])
def weatherpost():

    location = request.form['location']
    location = location.upper()
    key = '5977480005743963cf86cfae93747357'
    result = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + key).json()
    time= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    temp_max = round(result['main']['temp_max'] - 273)
    temp_min = round(result['main']['temp_min'] - 273)
    temp = round(result['main']['temp'] - 273)
    temp_feelslike = round(result['main']['feels_like'] - 273)
    humidity = result['main']['humidity']
    main_weather = result["weather"][0]['main']
    description = result["weather"][0]['description']
    wind_speed = result["wind"]['speed']

    response = {
        "location": location,
        "time": time,
        "temperature": temp,
        "sky": main_weather,
        "sky description": description,
        "temperature feels like": temp_feelslike,
        "minimum temperature": temp_min,
        "maximum temperature": temp_max,
        "humidity level": humidity,
        "wind speed": wind_speed
    }

    #db.weather.insert_one(response)
    return render_template('weather.html', data=response)


@app.route("/weather")
def start():
    return render_template("indexweather.html")


if __name__ == "__main__":
    app.run()
