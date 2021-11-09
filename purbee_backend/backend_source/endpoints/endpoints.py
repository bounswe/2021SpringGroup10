import json

import pymongo
import requests
from flask import Flask, request

from purbee_backend.backend_source.login.login import (
    sign_up,
    sign_in
)

FORBIDDEN_STATUS_CODE = 403
SUCCESS_STATUS_CODE = 200
DATABASE_UPDATED_STATUS_CODE = 201

USER_NAME = ""
USER_PASSWORD = ""

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.dbcb9.mongodb.net/first".format(USER_NAME, USER_PASSWORD))
db = client.first
db_registered_users = db.registered_users


@app.route('/sign_up/', methods=['POST'])
def sign_up_endpoint():
    req = request.get_json()
    content = json.dumps(req)

    res = requests.Response()
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers[
        'Access-Control-Allow-Headers'] = 'access-control-allow-headers,access-control-allow-methods,access-control-allow-origin,content-type'
    res.headers['Content-Type'] = 'application/json'
    data = {"response_message": None}
    status_code = None

    return_status = sign_up(**content)

    if return_status == 0:
        data["response_message"] = "User successfully signed up."
        status_code = DATABASE_UPDATED_STATUS_CODE
    elif return_status == 1:
        data["response_message"] = "User name already exists."
        status_code = FORBIDDEN_STATUS_CODE
    elif return_status == 2:
        data["response_message"] = "E-mail address already exists."
        status_code = FORBIDDEN_STATUS_CODE
    elif return_status == 3:
        data["response_message"] = "Password is not secure enough."
        status_code = FORBIDDEN_STATUS_CODE

    return data, status_code, res.headers


@app.route('/sign_in/', methods=['GET'])
def sign_in_endpoint():
    req = request.get_json()
    content = json.dumps(req)

    res = requests.Response()
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers[
        'Access-Control-Allow-Headers'] = 'access-control-allow-headers,access-control-allow-methods,access-control-allow-origin,content-type'
    res.headers['Content-Type'] = 'application/json'
    data = {"Response Message": None}
    status_code = None

    return_status = sign_in(**content)

    if return_status == 0:
        status_code = SUCCESS_STATUS_CODE
        data["response_message"]  = "Successfully signed in."
        data["user_name"] = content["user_name"]
    elif return_status == 1:
        pass



