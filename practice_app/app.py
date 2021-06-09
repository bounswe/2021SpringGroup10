from flask import Flask, render_template, request, redirect, jsonify, abort
import pymongo
import requests
from slackclient import SlackClient
import json
from helpers import helper_functions
from bson.objectid import ObjectId
import datetime


CHANNEL_ID = "C0242LA1NCS"
SLACK_TOKEN = "LATER NEEDS TO BE OBTAINED FROM ENV"
slack_client = SlackClient(SLACK_TOKEN)
DECATHLON_URL = 'https://sports.api.decathlon.com/sports/'
MOVIES_URL = "https://rickandmortyapi.com/api/character/30"
CATFACTS_URL='https://dog-facts-api.herokuapp.com/api/v1/resources/dogs/all'


joke_user = [
    False,
    "none",
    []
]

joke = [
    {
        "setup": "none",
        "punchline": "none"
    }
]

joke_first = [True]
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
joke_collection = db.joke
sportevent_collection = db.safa
messages_collection = db.messages
collectiondictionary = db.word

market_collection = db.berkay
movie_collection = db.movie
cat_collection = db.catfacts
news_collection = db.news



collectionkey = db.key
apikeyx = collectionkey.find_one({"keyword":"thekey"})
apikey = apikeyx["thekey"]



#------News-----#

@app.route('/news/saved', methods=['POST', 'GET'])
def news_saved():
    if request.method == "GET":
        my_news = news_collection.find({})
        lst = []
        for e in my_news:
            tmp = {"source": e["source"],
            "title": e["title"],
            "description": e["description"],
            "date": e["date"],
            "url": e["url"]}
            lst.append(tmp)
            
        return jsonify({"My Pocket": lst})

    elif request.method == "POST":
        req = request.values.to_dict()
        if not req:
            req = request.json

        my_new_news = {"_id":req["title"],
        "source":req["source"],
        "title":req["title"],
        "description":req["description"],
        "date":req["date"],
        "url":req["url"]}

        try:
            news_collection.insert_one(my_new_news)
        except Exception as e:
            return "Failed"
        return "Success"


@app.route('/news/fetch', methods=['GET'])
def news_fetch():
    s_keyword = request.form.get("keywords")
    # IndexedNews.query.delete()
    API_KEY = "10689593098485c096e61e8dbfc4ac92"
    url = "http://api.mediastack.com/v1/news?access_key=%s" % API_KEY
    limit = "&limit=100"
    sources = "&sources=%s" % "nytimes,bbc,guardian"
    if s_keyword:
        keywords = "&keywords=%s" % s_keyword
    else:
        keywords = ""
    languages = "&lanuages=en,-ar,-de,-es,-fr,-he,-it,-nl,-no,-pt,-ru,-se,-zh"
    url = url + keywords + limit + languages + sources
    response = requests.get(url)
    dict = response.json()
    new_dict = {}
    news_list = []
    for news in dict["data"]:
        news["description"] = "No Description" if not news["description"] else news["description"]
        tmp_dict = {"title": news["title"],
                    "description": news["description"],
                    "date": news["published_at"],
                    "url": news["url"],
                    "source": news["source"]}
        news_list.append(tmp_dict)

    new_dict["News"] = news_list
    return jsonify(new_dict)


@app.route('/news', methods=['GET', 'POST'])
def news_index():
    if request.method == 'POST':
        res = requests.get("http://127.0.0.1:5000/news/fetch", data={'keywords': request.form['keywords']}).json()
        return render_template('news_index.html', news=res["News"])

    if request.method == 'GET':
        response = requests.get("http://127.0.0.1:5000/news/fetch")
        resp = response.json()
        return render_template('news_index.html', news=resp["News"])


@app.route('/news/pocket', methods=['GET', 'POST'])
def news_pocket():
    if request.method == 'POST':
        params = {'source': request.form['source'],
                  'title': request.form['title'],
                  'description': request.form['description'],
                  'date': request.form['date'],
                  'url': request.form['url']}
        res = requests.post("http://127.0.0.1:5000/news/saved",data= params)
        return redirect("/news/pocket")

    elif request.method == 'GET':
        response = requests.get("http://127.0.0.1:5000/news/saved")
        resp = response.json()
        return render_template('news_pocket.html', news=resp["My Pocket"])



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
            api_response.append(response[i]['fact'])
        

     

        return render_template('catfacts.html', cat_facts = cat_facts, cat_facts_api=api_response)



@app.route('/api/v1.0/catfacts', methods = ["GET", "POST"])
def cat_facts_api():
    
    if request.method == "POST":
        if not request.json or not 'fact' in request.json:
            abort(400)
        fact = request.json["fact"]
        
      
        try:
            cat_collection.insert_one({'fact': fact})
          
            return {'fact':fact} ,201
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
          
            return {'mmovie':mmovie} ,201
        except:
          
             return {'data': "there is an error"}
    else:

        movies = movie_collection.find({})
        
        json_objects = []
        for mmovie in movies:
            json_objects.append({'mmovie': mmovie["mmovie"]})
        return {'data': json_objects}



@app.route('/api/v1.0/movie/<int:_id>', methods = ["GET"])
def get_movie(_id):
    
    mmovie = movie_collection.get_or_404(_id)
        
    return {'data': {'_id': mmovie._id, 'text': mmovie.text}}, 200


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


@app.route("/market" ,methods = ["GET","POST"])
def marketHome():
    if request.method == "POST":
        return redirect("/market/getLastDaysForStock",code=307)
    return render_template('home_market.html')


@app.route("/market/getCurrenciesNames", methods = ["GET"])
def getCurrenciesLastPrice():
    response = requests.get("http://api.marketstack.com/v1/currencies?access_key=10818e5bb1090fefbd86603de2ab9d0c" ).json()
    dict = {}
    for i in response['data']:
        dict[i["code"]] = i["name"]
    return render_template("result_market.html",result = dict)


@app.route('/market/getLastDaysForStock', methods=["POST"])
def getLastDaysForStock():
    stockName = request.form["Name"]
    Day = request.form["day"]
    url = "http://api.marketstack.com/v1/eod?access_key=10818e5bb1090fefbd86603de2ab9d0c&symbols="+stockName
    response = requests.get(url).json()
    dict = {}
    j=0
    for i in response['data']:
        response = requests.post("http://127.0.0.1:5000/market/save/{}/{}/{}".format(i["date"][:10],stockName,str(i["close"])+" $"))
        dict[i["date"][:10]] = str(i["close"])+" $"
        j=j+1
        if j== int(Day):
            break
    return render_template('result_market.html', result=dict)

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


@app.route('/dictionary')
def home_dictionary():
    return render_template('search.html')


@app.route("/dictionary-search-synonym/<word>", methods=["GET"])
def synonym_dictionary(word):
    url_synonym = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/synonyms"
    headers_synonym = {
        'x-rapidapi-key': apikey,
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
        'x-rapidapi-key': apikey,
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





@app.route('/joke/add_user/<user_name>', methods=["POST"])
def joke_add_user(user_name):
    if request.method == "POST":
        return helper_functions.add_user(user_name, joke_collection)
    else:
        return None


@app.route('/joke/get_user/<user_name>', methods=["GET"])
def joke_get_user(user_name):
    if request.method == "GET":
        return helper_functions.get_user(user_name, joke_collection)
    else:
        return None


@app.route('/joke/delete_user/<user_name>', methods=["DELETE"])
def joke_delete_user(user_name):
    if request.method == "DELETE":
        return helper_functions.delete_user(user_name, joke_collection)
    else:
        return None


@app.route('/joke/add_to_list/<user_name>/<set_up>/<punch_line>', methods=["GET", "PUT"])
def joke_add_to_list(user_name, set_up, punch_line):
    if request.method == "PUT":
        return helper_functions.add_to_list(user_name, set_up, punch_line, joke_collection)
    else:
        return None


@app.route('/joke/', methods=["GET", "POST"])
def joke_home():
    joke_first[0] = True
    if request.method == "POST":
        user_response = requests.get('http://127.0.0.1:5000/joke/get_user/{}'.format(request.form['user']))
        if user_response.status_code == 200:
            user_result = user_response.json()
            joke_user[0] = True
            joke_user[1] = request.form['user']
            joke_user[2] = user_result['jokes']
        else:
            joke_user[1] = request.form['user']
            add_response = requests.post('http://127.0.0.1:5000/joke/add_user/{}'.format(request.form['user']))
            joke_user[0] = True
        return redirect('/joke/choice'.format(request.form['user']))

    return render_template('joke_home.html')


@app.route('/joke/user/<wish>', methods=["GET", "POST"])
def joke_user_wish(wish):
    if joke_user[0]:
        if wish == "make":
            if joke_first[0]:
                joke_response = requests.get("https://official-joke-api.appspot.com/random_joke")
                joke_json = joke_response.json()
                joke[0] = joke_json
                joke_first[0] = False

            if request.method == "POST":
                joke1 = joke[0]['setup'].replace("?", "_")
                joke2 = joke[0]['punchline'].replace("?", "_")
                add_to_list_response = requests.put('http://127.0.0.1:5000/joke/add_to_list/{}/{}/{}'.format(joke_user[1], joke1, joke2))
                return redirect('/joke/user/show')
            if joke[0]['setup'] == "none":
                joke_first[0] = True
            return render_template("joke_make_joke.html", data=joke[0])
        elif wish == "show":
            joke_first[0] = True
            user_response = requests.get('http://127.0.0.1:5000/joke/get_user/{}'.format(joke_user[1]))
            joke_user[2] = user_response.json()['jokes']
            return render_template("joke_show_jokes.html", data=joke_user[2])
        else:
            return redirect('/joke/')
    else:
        return redirect('/joke/')


@app.route('/joke/choice', methods=["GET", "POST"])
def joke_choice():
    joke_first[0] = True
    if request.method == "POST":
        if request.form["joke"] == "Make a Joke" or request.form["joke"] == "Show my Jokes":
            return redirect('/joke/user/{}'.format(request.form["joke"].split()[0]).lower())
        else:
            return redirect('/joke')

    return render_template("joke_choice.html")




@app.route("/write2us", methods=['POST', 'GET'])
def write_to_channel():
    try:
        if request.method == "POST":
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            message = request.form.get("message")
            response = write_to_channel_with_params(fname, lname, message)
            return "<p>Your message has reached to our slack channel! You can check if someone from our team replied to your message with the id: <b>{}</b></p><br>You have to save this id if you would like to check later that your message had replied by someone from our team".format(response["id"])
    except:
        return "<p>Something went wrong</p>", 400
    return render_template("write2us.html")


@app.route("/write2channel/<fname>/<lname>/<message>", methods=['POST'])
def write_to_channel_with_params(fname, lname, message):
    try:
        formatted_message=str(fname) + " " + lname + ": " + str(message)
        message = slack_client.api_call(
            "chat.postMessage",
            channel=CHANNEL_ID,
            text=formatted_message,
            username='write2us bot',
            icon_emoji=':robot_face:'
        )
        thread_ts = message["ts"]
        _id = messages_collection.insert({'thread_ts': thread_ts, 'fname': fname, 'lname': lname})
        return {"id": str(_id)}
    except:
        raise Exception("Something went wrong while sending the message. Please try again.")



@app.route("/slack-reply", methods=['GET', 'POST'])
def check_reply():
    try:
        if request.method == "POST":
            mid = request.form.get("mid")
            all_replies = check_replies(mid)
            if len(all_replies["replies"]) > 0:
                return render_template('display-messages.html', data=all_replies["replies"])
            else:
                return "<p>No one replied to your message yet.</p>"
        return render_template('check-my-replies.html')
    except:
        return "<p>Invalid ID!</p>"

@app.route("/slack-replies/<conversation_id>", methods=['GET'])
def check_replies(conversation_id):
    try:
        doc = messages_collection.find_one({'_id': ObjectId(conversation_id)})
        replies = slack_client.api_call("conversations.replies", channel=CHANNEL_ID, ts=doc["thread_ts"])
        if len(replies['messages']) > 1:
            all_replies = []
            for reply in replies['messages']:
                message = reply['text']
                replier = slack_client.api_call("users.info", user=replies['messages'][1]['user'])
                replier_real_name = replier['user']['real_name']
                all_replies.append({"replier": replier_real_name, "message": message})
            all_replies.pop(0)
            return {"replies": all_replies}
        else:
            return {"replies": []}
    except:
        raise Exception("Invalid message id")



if __name__ == '__main__':
    app.run(debug=True)
