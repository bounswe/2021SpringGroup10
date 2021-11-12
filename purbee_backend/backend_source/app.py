import json
import sys
import pymongo
import requests
from flask import Flask, request, Response

from purbee_backend.backend_source.login.login import (
    sign_up,
    sign_in
)

SC_FORBIDDEN = 403
SC_SUCCESS = 200
SC_CREATED = 201
SC_UNAUTHORIZED = 401
USER_NAME = ""
USER_PASSWORD = ""

app = Flask(__name__)



@app.route('/sign_up/', methods=['POST'])
def sign_up_endpoint():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    return_status = sign_up(**req)
    if return_status == 0:
        data["response_message"] = "User successfully signed up."
        status_code = SC_CREATED
    elif return_status == 1:
        data["response_message"] = "User name already exists."
        status_code = SC_FORBIDDEN
    elif return_status == 2:
        data["response_message"] = "E-mail address already exists."
        status_code = SC_FORBIDDEN
    elif return_status == 3:
        data["response_message"] = "Password is not secure enough."
        status_code = SC_FORBIDDEN

    return data, status_code


@app.route('/sign_in/', methods=['GET'])
def sign_in_endpoint():
    req = request.get_json()
    data = {"Response Message": None}
    status_code = None
    return_status = sign_in(**req)

    if return_status == 0:
        status_code = SC_SUCCESS
        data["response_message"] = "Successfully signed in."
        data["user_name"] = req["user_name"]
    elif return_status == 1:
        status_code = SC_UNAUTHORIZED
        data["response_message"] = "Credentials are incorrect"
        data["user_name"] = None

    return data, status_code



if __name__ == '__main__':
    app.run(debug=True)
