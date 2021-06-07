from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json

app = Flask(__name__)
app.config[ 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

DECATHLON_URL = 'https://sports.api.decathlon.com/sports/'


class SportEvent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sport_type = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(200), nullable = True)



@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/sportevents', methods = ['GET', 'POST'])
def sport_events():
    if request.method == "POST":
        sport_type = request.form["sport_type"]
        description = request.form["description"]
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/sportevents"
        headers = {'Content-type': 'application/json'}

        task = {"sport_type": sport_type, "description": description}

        response = requests.post(req, data=json.dumps(task), headers=headers)
        return redirect('/sportevents')
    else:
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/sportevents"
        headers = {'Content-type': 'application/json'}
        response = requests.get(req).json()
        sport_events = response['data']

        return render_template('sportevents.html', sport_events = sport_events)


@app.route('/api/v1.0/sportevents', methods = ["GET", "POST"])
def sport_events_api():
    if request.method == "POST":
        if not request.json or not 'sport_type' in request.json:
            abort(400)
        sport_type = request.json["sport_type"]
        try:
            description = request.json["description"]
        except:
            description = ''
        sport_event = SportEvent(sport_type = sport_type, description = description)
        
        try:
            db.session.add(sport_event)
            db.session.commit()
            if sport_event.description == "":
                type = str(sport_event.sport_type).lower()
                response = requests.get(DECATHLON_URL+type).json()
                desc = response["data"]["attributes"]["description"]
                sport_event.description = desc
            return {'data': {'id': sport_event.id, 'sport_type': sport_event.sport_type, 'description': sport_event.description}}, 201
        except:
            return "There was an issue adding your sport event"
    else:
        sport_events = SportEvent.query.order_by(SportEvent.id).all()
        json_objects = []
        for event in sport_events:
            if event.description == "":
                type = str(event.sport_type).lower()
                response = requests.get(DECATHLON_URL+type).json()
                desc = response["data"]["attributes"]["description"]
                event.description = desc
            json_objects.append({'id': event.id, 'sport_type': event.sport_type, 'description': event.description})
        return jsonify({'data': json_objects}), 200

@app.route('/api/v1.0/sportevents/<int:id>', methods = ["GET"])
def get_single_event(id):
    event = SportEvent.query.get_or_404(id)
    if event.description == "":
        type = str(event.sport_type).lower()
        response = requests.get(DECATHLON_URL+type).json()
        desc = response["data"]["attributes"]["description"]
        event.description = desc
        
    return {'data': {'id': event.id, 'sport_type': event.sport_type, 'description': event.description}}, 200



if __name__ == "__main__":
    app.run(debug=True)