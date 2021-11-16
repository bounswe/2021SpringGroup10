from flask import Flask, request


from login.login import (
    sign_up,
    sign_in,
    update_profile_page,
    get_profile_page
)

SC_FORBIDDEN = 403
SC_SUCCESS = 200
SC_CREATED = 201
SC_UNAUTHORIZED = 401
SC_BAD_REQUEST = 400
USER_NAME = ""
USER_PASSWORD = ""

app = Flask(__name__)


@app.route('/api/sign_up/', methods=['POST'])
def sign_up_endpoint():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    try:
        return_status = sign_up(**req)
    except:
        data["response_message"] = "Incorrect json content. (necessary fields are mail_address,user_name,password)"
        status_code = SC_BAD_REQUEST
        return data, status_code
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


@app.route('/api/sign_in/', methods=['GET'])
def sign_in_endpoint():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    try:
        return_status = sign_in(**req)
    except:
        data["response_message"] = "Incorrect json content. (necessary fields are user_name,password)"
        status_code = SC_BAD_REQUEST
        return data, status_code
    if return_status == 0:
        return_dic = {"user_name": req["user_name"]}
        status_code = SC_SUCCESS
        data["response_message"] = "Successfully signed in."
        data["data"] = return_dic
    elif return_status == 1:
        return_dic = {"user_name": None}
        status_code = SC_UNAUTHORIZED
        data["response_message"] = "Credentials are incorrect"
        data["data"] = return_dic

    return data, status_code


@app.route('/api/profile_page/', methods=['POST', 'GET'])
def profile_page():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    try:
        user_name = req["user_name"]
    except:
        data["response_message"] = "user_name is not specified."
        status_code = SC_BAD_REQUEST
        return data, status_code

    if request.method == "POST":
        return_status = update_profile_page(user_name, req)
        if return_status == 0:
            data["response_message"] = "User page updated successfully."
            status_code = SC_SUCCESS
        elif return_status == 1:
            data["response_message"] = "No such user."
            status_code = SC_BAD_REQUEST
        elif return_status == 2:
            data["response_message"] = "Database error occurred."
            status_code = SC_FORBIDDEN

        return data, status_code

    if request.method == "GET":
        db_return = get_profile_page(user_name)
        if db_return == 2:
            data["response_message"] = "Database error occurred."
            status_code = SC_FORBIDDEN
        elif db_return == 1:
            data["response_message"] = "No such user."
            status_code = SC_BAD_REQUEST
        else:
            data["response_message"] = "Profile page is successfully returned. "
            data["data"] = db_return
            status_code = SC_SUCCESS
        return data, status_code



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
