from flask import Flask, request, render_template, redirect
import pymongo
import requests
from slackclient import SlackClient
from helpers import helper_functions
from bson.objectid import ObjectId

app = Flask(__name__)

mongo_client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = mongo_client.first
joke_collection = db.joke
messages_collection = db.messages

CHANNEL_ID = "C0242LA1NCS"
SLACK_TOKEN = "xoxb-1881747695606-2138926157411-FDZY3FJ8wZNTJQDTR8La3Y46"

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


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form['button'] == 'joke':
            return redirect('/joke/')

    return render_template("home.html")


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