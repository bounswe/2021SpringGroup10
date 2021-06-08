from flask import Flask, render_template, request, redirect, jsonify
import pymongo
import requests
import json

app = Flask(__name__)
# app.config[ 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
# db = SQLAlchemy(app)

client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
sportevent_collection = db.safa


DECATHLON_URL = 'https://sports.api.decathlon.com/sports/'



@app.route('/api/v1.0/sportevents', methods = ["GET", "POST"])
def sport_events_api():
    if request.method == "POST":
        if not request.json or not 'sport_type' in request.json or not 'event_name' in request.json:
            abort(400)
        event_name = request.json["event_name"]
        sport_type = request.json["sport_type"]
        try:
            description = request.json["description"]
        except:
            description = ''
        sport_event = {'event_name': event_name, 'sport_type': sport_type, 'description': description}
        
        try:
            sportevent_collection.insert_one(sport_event)
            if sport_event["description"] == "":
                type = str(sport_event["sport_type"]).lower()
                response = requests.get(DECATHLON_URL+type).json()
                desc = response["data"]["attributes"]["description"]
                sport_event["description"] = desc
            return {'data': {'event_name': sport_event["event_name"], 'sport_type': sport_event["sport_type"], 'description': sport_event["description"]}}, 201
        except:
            return "There was an issue adding your sport event"
    else:
        sport_events = sportevent_collection.find({})
        json_objects = []
        for event in sport_events:
            if event["description"] == "":
                type = str(event["sport_type"]).lower()
                response = requests.get(DECATHLON_URL+type).json()
                desc = response["data"]["attributes"]["description"]
                event["description"] = desc
            json_objects.append({'event_name': event["event_name"], 'sport_type': event["sport_type"], 'description': event["description"]})
        return jsonify({'data': json_objects}), 200

@app.route('/api/v1.0/sportevents/<sport_type>', methods = ["GET"])
def get_single_event(sport_type):
    sport_type = sport_type.lower()
    sport_events = sportevent_collection.find({"sport_type": sport_type})
    json_objects = []
    for event in sport_events:
        if event["description"] == "":
            type = str(event["sport_type"]).lower()
            response = requests.get(DECATHLON_URL+type).json()
            desc = response["data"]["attributes"]["description"]
            event["description"] = desc
        json_objects.append({'event_name': event["event_name"], 'sport_type': event["sport_type"], 'description': event["description"]})
    return jsonify({'data': json_objects}), 200

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/sportevents', methods = ['GET', 'POST'])
def sport_events():
    if request.method == "POST":
        event_name = request.form["event_name"]
        sport_type = request.form["sport_type"].lower()
        description = request.form["description"]
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/sportevents"
        headers = {'Content-type': 'application/json'}

        event = {"event_name": event_name, "sport_type": sport_type, "description": description}

        response = requests.post(req, data=json.dumps(event), headers=headers)
        return redirect('/sportevents')
    else:
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/sportevents"
        headers = {'Content-type': 'application/json'}
        response = requests.get(req).json()
        sport_events = response['data']
        return render_template('sportevents.html', sport_events = sport_events)



if __name__ == "__main__":
    app.run(debug=True)