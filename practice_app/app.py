from flask import Flask, request, render_template, redirect, jsonify
import requests
import pymongo
import datetime


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first


@app.route('/weathergetindex', methods=['GET'])
def weathergetindex():
    result = requests.get("http://127.0.0.1:5000/weatherget")
    return render_template('weatherGet.html', data=result.json())


@app.route('/weatherget', methods=['GET'])
def weatherget():
    response = db.weather.find().sort("time", -1)
    result = response[0]
    result.pop('_id')
    return result


@app.route('/weatherpostindex/<string:location>', methods=['GET'])
def weatherpostindex(location):

    response = requests.post("http://127.0.0.1:5000/weatherpost/{}".format(location)).json()
    if response != "Please enter a valid location":
        db.weather.insert_one(response)
    return render_template('weather.html', data=response)


@app.route("/weatherpost/<string:location>", methods=['POST'])
def weatherpost(location):

    try:
        key = '5977480005743963cf86cfae93747357'
        result = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + key).json()
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

        return response
    except Exception as e:
        return jsonify("Please enter a valid location")


@app.route("/weather", methods=['GET', 'POST'])
def start():

    if request.method != 'GET':
        res = request.form["getorpost"]
        if res == "OK":
            return redirect('/weathergetindex')
        else:
            location = request.form['location']
            location = location.upper()
            return redirect('/weatherpostindex/{}'.format(location))

    return render_template("indexweather.html")


if __name__ == "__main__":
    app.run()
