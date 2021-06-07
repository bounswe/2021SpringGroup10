from flask import Flask, request, render_template, redirect
import requests
import pymongo
import datetime


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://baseuser:baseuser@cluster0.cjzn1.mongodb.net/352api?"
                             "retryWrites=true&w=majority")
db = client["352api"]


@app.route('/weathergetindex', methods=['GET'])
def weathergetindex():
    result = requests.get("http://127.0.0.1:5000/weatherget").json()
    return render_template('weatherGet.html', data=result)


@app.route('/weatherget', methods=['GET'])
def weatherget():
    response = db.weather.find().sort("time", -1)

    for result in response:
        temp = result.pop('_id')
        return result
        break


@app.route('/weatherpostindex/<string:location>', methods=['GET'])
def weatherpostindex(location):

    response = requests.post("http://127.0.0.1:5000/weatherpost/{}".format(location)).json()
    db.weather.insert_one(response)
    return render_template('weather.html', data=response)


@app.route("/weatherpost/<string:location>", methods=['POST'])
def weatherpost(location):

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
