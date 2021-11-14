import json
import sys
import pymongo
import requests
from flask import Flask, request, Response

from purbee_backend.backend_source.login.login import (
    sign_up,
    sign_in,
    update_profile_page,
    get_profile_page
)

SC_FORBIDDEN = 403
SC_SUCCESS = 200
SC_CREATED = 201
SC_UNAUTHORIZED = 401
SC_BADREQUEST = 400
USER_NAME = ""
USER_PASSWORD = ""

app = Flask(__name__)


@app.route('/sign_up/', methods=['POST'])
def sign_up_endpoint():
    req = request.get_json()
    data = {"Response Message": None}
    status_code = None
    try:
        return_status = sign_up(**req)
    except:
        data["Response Message"] = "Incorrect json content. (necessary fields are mail_address,user_name,password)"
        status_code = SC_BADREQUEST
        return data, status_code
    if return_status == 0:
        data["Response Message"] = "User successfully signed up."
        status_code = SC_CREATED
    elif return_status == 1:
        data["Response Message"] = "User name already exists."
        status_code = SC_FORBIDDEN
    elif return_status == 2:
        data["Response Message"] = "E-mail address already exists."
        status_code = SC_FORBIDDEN
    elif return_status == 3:
        data["Response Message"] = "Password is not secure enough."
        status_code = SC_FORBIDDEN

    return data, status_code


@app.route('/sign_in/', methods=['GET'])
def sign_in_endpoint():
    req = request.get_json()
    data = {"Response Message": None}
    status_code = None
    try:
        return_status = sign_in(**req)
    except:
        data["Response Message"] = "Incorrect json content. (necessary fields are user_name,password)"
        status_code = SC_BADREQUEST
        return data, status_code
    if return_status == 0:
        status_code = SC_SUCCESS
        data["Response Message"] = "Successfully signed in."
        data["user_name"] = req["user_name"]
    elif return_status == 1:
        status_code = SC_UNAUTHORIZED
        data["Response Message"] = "Credentials are incorrect"
        data["user_name"] = None

    return data, status_code

@app.route('/profile_page/', methods=['POST','GET'])
def profile_page():
    print("resultDict2", file=sys.stderr)
    req = request.get_json()
    data = {"Response Message": None}
    status_code = None
    user_name = ""
    profile_photo = []
    bio = ""
    first_name = ""
    last_name = ""
    birth_date = ""
    if "user_name" in req:
        user_name = req["user_name"]
    if "profile_photo" in req:
        profile_photo = req["profile_photo"]
    if "bio" in req:
        bio = req["bio"]
    if "first_name" in req:
        first_name = req["first_name"]
    if "last_name" in req:
        last_name = req["last_name"]
    if "birth_date" in req:
        birth_date = req["birth_date"]

    if request.method == "POST":
        print("resultDict3", file=sys.stderr)
        return_status = update_profile_page(user_name,profile_photo,bio,first_name,last_name,birth_date)
        if return_status == 0:
            data["Response Message"] = "User page updated successfully."
            status_code = SC_SUCCESS
        elif return_status == 1:
            data["Response Message"] = "No such user."
            status_code = SC_BADREQUEST
        elif return_status == 2:
            data["Response Message"] = "Database error occurred."
            status_code = SC_FORBIDDEN

        return data, status_code
    resultDict = {}
    if request.method == "GET":
        return_status = get_profile_page(user_name)
        print(return_status, file=sys.stderr)
        if return_status == 2:
            data["Response Message"] = "Database error occurred."
            status_code = SC_FORBIDDEN
        elif return_status == 1:
            data["Response Message"] = "No such user."
            status_code = SC_BADREQUEST
        else:
            resultDict['profile_photo'] = return_status[0]
            resultDict['following'] = return_status[1]
            resultDict['followers'] = return_status[2]
            resultDict['first_name'] = return_status[3]
            resultDict['last_name'] = return_status[4]
            resultDict['birth_date'] = return_status[5]
            resultDict['post_list'] = return_status[6]
            resultDict['user_name'] = user_name
            data["Response Message"] = json.dumps(resultDict)
            status_code = SC_SUCCESS
        return data, status_code






if __name__ == '__main__':
    app.run(debug=True)
