import collections
from flask import Flask
import requests
from requests.sessions import Request
from flask import Flask, url_for
from flask import Flask, request, redirect
from flask import render_template
import json
import pymongo
import sys


app = Flask(__name__)


client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
movie_collection = db.movie

MOVIES_URL = "https://rickandmortyapi.com/api/character/30"

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/movies', methods = ['GET', 'POST'])
def movies():
    if request.method == "POST":
       
        text = request.form["text"]
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/movie"
        headers = {'Content-type': 'application/json'}

        mmovie = {"mmovie": text}

        response = requests.post(req, data=json.dumps(mmovie), headers=headers)
        return redirect('/movies')
    else:
        endpoint = "http://127.0.0.1:5000"

        req = endpoint + "/api/v1.0/movie"
        headers = {'Content-type': 'application/json'}
        response = requests.get(req).json()
        movies=response['data']
        print(movies)
        
        
        headers = {'Content-type': 'application/json'}
        response = requests.get(MOVIES_URL).json()
        
        api_response=[response['name'],response['species']]
       
        
        
        

     

        return render_template('movies.html', movies = movies, movies_api=api_response)



@app.route('/api/v1.0/movie', methods = ["GET", "POST"])
def movies_api():
    
    if request.method == "POST":
        if not request.json or not 'mmovie' in request.json:
            abort(400)
        mmovie = request.json["mmovie"]
        
      
        try:
            movie_collection.insert_one({'mmovie': mmovie})
          
            return {'mmovie':mmovie}
        except:
          
             return {'data': "there is an error"}
    else:

        movies = movie_collection.find({})
        
        json_objects = []
        for mmovie in movies:
            json_objects.append({'mmovie': mmovie["mmovie"]})
        print(json_objects)
        return {'data': json_objects}



@app.route('/api/v1.0/movie/<int:_id>', methods = ["GET"])
def get_movie(_id):
    
    mmovie = movie_collection.get_or_404(_id)
        
    return {'data': {'_id': mmovie._id, 'text': mmovie.text}}, 200



if __name__ == "__main__":
    app.run(debug=True)

