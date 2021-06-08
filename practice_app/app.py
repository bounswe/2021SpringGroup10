from flask import Flask, request, render_template, redirect
import pymongo
import requests
from helpers import helper_functions

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://base_user:base_user_password@cluster0.dbcb9.mongodb.net/first")
db = client.first
joke_collection = db.joke

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


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form['button'] == 'joke':
            return redirect('/joke/')

    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
