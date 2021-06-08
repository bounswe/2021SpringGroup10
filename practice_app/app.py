from typing import Text
from flask import Flask, render_template, request, redirect

import pymongo
from flask_restful import  abort

import requests
import json

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
cat_collection = db.catfacts

CATFACTS_URL='https://cat-fact.herokuapp.com/facts'



@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/catfacts', methods = ['GET', 'POST'])
def cat_facts():
    if request.method == "POST":
       
        text = request.form["text"]
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/catfacts"
        headers = {'Content-type': 'application/json'}

        fact = {"fact": text}

        response = requests.post(req, data=json.dumps(fact), headers=headers)
        return redirect('/catfacts')
    else:
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/catfacts"
        headers = {'Content-type': 'application/json'}
        response = requests.get(req).json()
        cat_facts=response['data']
        
        
        
        headers = {'Content-type': 'application/json'}
        response = requests.get(CATFACTS_URL).json()
        
        api_response=[]

        for i in range(5):
            api_response.append(response[i]['text'])
        

     

        return render_template('catfacts.html', cat_facts = cat_facts, cat_facts_api=api_response)



@app.route('/api/v1.0/catfacts', methods = ["GET", "POST"])
def cat_facts_api():
    
    if request.method == "POST":
        if not request.json or not 'fact' in request.json:
            abort(400)
        fact = request.json["fact"]
        
      
        try:
            cat_collection.insert_one({'fact': fact})
          
            return {'fact':fact}
        except:
          
             return {'data': "there is an error"}
    else:

        cat_facts = cat_collection.find({})
        
        json_objects = []
        for fact in cat_facts:
            json_objects.append({'fact': fact["fact"]})
        
        return {'data': json_objects}
      


@app.route('/api/v1.0/catfacts/<int:_id>', methods = ["GET"])
def get_cat_fact(_id):
    
    fact = cat_collection.get_or_404(_id)
        
    return {'data': {'_id': fact._id, 'text': fact.text}}, 200




# @app.route('/delete/<int:_id>')
# def delete(_id):
#     cat_fact_delete = cat_collection.get_or_404(_id)

#     try:
#         db.session.delete(cat_fact_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return {'data': "there is an error"}




if __name__ == "__main__":
    app.run(debug=True)