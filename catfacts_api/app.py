from typing import Text
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  abort
from datetime import datetime
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
CATFACTS_URL='https://cat-fact.herokuapp.com/facts'

class Catfacts(db.Model):
    _id = db.Column(db.String(24), primary_key=True)
    text = db.Column(db.String(500), nullable=False)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/catfacts', methods = ['GET', 'POST'])
def cat_facts():
    if request.method == "POST":
        _id = request.form["_id"]
        text = request.form["text"]
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/catfacts"
        headers = {'Content-type': 'application/json'}

        task = {"_id": _id, "text": text}

        response = requests.post(req, data=json.dumps(task), headers=headers)
        return redirect('/catfacts')
    else:
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/catfacts"
        headers = {'Content-type': 'application/json'}
        response = requests.get(req).json()
        cat_facts = response['data']

        return render_template('catfacts.html', cat_facts = cat_facts)



@app.route('/api/v1.0/catfacts', methods = ["GET", "POST"])
def cat_facts_api():
    if request.method == "POST":
        if not request.json or not 'text' in request.json:
            abort(400)
        text = request.json["text"]
        
        cat_facts = Catfacts(text = text)
        
        try:
            db.session.add(cat_facts)
            db.session.commit()
           
            return {'data': {'_id': cat_facts._id, 'text': cat_facts.text}}, 201
        except:
            return "There was an issue adding new catfact"
    else:
        cat_facts = Catfacts.query.order_by(Catfacts._id).all()
        json_objects = []
        for fact in cat_facts:
            json_objects.append({'_id': fact._id, 'text': fact.text})
        return jsonify({'data': json_objects}), 200


@app.route('/api/v1.0/catfacts/<str:_id>', methods = ["GET"])
def get_cat_fact(_id):
    fact = Catfacts.query.get_or_404(_id)
        
    return {'data': {'_id': fact._id, 'text': fact.text}}, 200




@app.route('/delete/<String:_id>')
def delete(_id):
    cat_fact_delete = Catfacts.query.get_or_404(id)

    try:
        db.session.delete(cat_fact_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that catfact'




if __name__ == "__main__":
    app.run(debug=True)