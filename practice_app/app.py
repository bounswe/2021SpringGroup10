
from typing import Text
from flask import Flask, render_template, request, redirect, jsonify,abort
import pymongo
import requests
from slackclient import SlackClient
import json
from helpers import helper_functions
from bson.objectid import ObjectId



CHANNEL_ID = "C0242LA1NCS"
SLACK_TOKEN = "xoxb-1881747695606-2138926157411-FDZY3FJ8wZNTJQDTR8La3Y46"
DECATHLON_URL = 'https://sports.api.decathlon.com/sports/'
CATFACTS_URL='https://cat-fact.herokuapp.com/facts'

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

client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
joke_collection = db.joke
sportevent_collection = db.safa
messages_collection = db.messages
cat_collection = db.catfacts




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
