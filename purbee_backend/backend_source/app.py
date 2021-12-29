from flask import Flask, request

from community.community import Community
from login.login import (
    sign_up,
    sign_in,
    update_profile_page,
    get_profile_page
)
from post.post import Post
from post.post_type import PostType

SC_FORBIDDEN = 403
SC_SUCCESS = 200
SC_CREATED = 201
SC_UNAUTHORIZED = 401
SC_BAD_REQUEST = 400
SC_INTERNAL_ERROR = 500
USER_NAME = ""
USER_PASSWORD = ""

app = Flask(__name__)


@app.route('/api/community_page/', methods=['POST', 'GET', 'PUT'])
def community_page():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    if request.method == "POST":
        needed_keys = ['id', 'is_private', 'community_creator_id']
        if len(needed_keys) != len(req):
            # return invalid input error
            data[
                'response_message'] = "Incorrect json content. (necessary fields are id, is_private, community_creator_id)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                data[
                    'response_message'] = "Incorrect json content. (necessary fields are id, is_private, community_creator_id"
                status_code = SC_BAD_REQUEST
                return data, status_code
        community_instance = Community(req)
        post_result = community_instance.save2database()
        if post_result == 0:
            # return success
            data['response_message'] = "Community Page successfully created."
            status_code = SC_CREATED
            return data, status_code
        elif post_result == 1:
            # return error: already have this community with community id
            data['response_message'] = "Community ID is already in use"
            status_code = SC_FORBIDDEN
            return data, status_code
        elif post_result == 2:
            # return internal error
            data['response_message'] = 'Internal Error'
            status_code = SC_INTERNAL_ERROR
            return data, status_code
    elif request.method == "GET":
        needed_keys = ['id']
        if len(needed_keys) != len(req):
            # return invalid input error
            data['response_message'] = "Incorrect json content. (necessary field is id)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                data['response_message'] = "Incorrect json content. (necessary field is id)"
                status_code = SC_BAD_REQUEST
                return data, status_code
        community_instance = Community.get_community_from_id(req['id'])
        if community_instance:
            # return success
            data['response_message'] = "Community successfully found"
            data['community_instance'] = community_instance.to_dict()
            status_code = SC_SUCCESS
            return data, status_code
        else:
            # return not found error
            data['response_message'] = "Specified community with the id not found"
            status_code = SC_FORBIDDEN
            return data, status_code
    elif request.method == "PUT":
        needed_keys = ['id', 'admin_list', 'subscriber_list', 'post_type_id_list', 'post_history_id_list',
                       'description',
                       'photo', 'community_creator_id', 'created_at', 'banned_user_list', 'is_private']
        if len(needed_keys) != len(req):
            # return invalid input error
            data['response_message'] = "Incorrect json content. (necessary field are the community class fields)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_key in req:
            if r_key in needed_keys:
                pass
            else:
                # return invalid input error
                data['response_message'] = "Incorrect json content. (necessary field are the community class fields)"
                status_code = SC_BAD_REQUEST
                return data, status_code
        community_instance = Community.get_community_from_id(req['id'])
        if community_instance:
            community_instance.update(req)
            community_dictionary = community_instance.to_dict()
            update_result = Community.update_on_database(community_dictionary)
            if update_result == 0:
                # return success
                data['response_message'] = "Community successfully updated"
                data['community_instance'] = community_dictionary
                status_code = SC_CREATED
                return data, status_code
            elif update_result == 1:
                # return internal error
                data['response_message'] = 'Internal Error'
                status_code = SC_INTERNAL_ERROR
                return data, status_code
        else:
            # not found user error
            data['response_message'] = "Specified community with the id not found"
            status_code = SC_FORBIDDEN
            return data, status_code


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


@app.route('/api/sign_in/', methods=['POST'])
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


@app.route('/api/post/', methods=['GET', 'POST', 'PUT'])
def post():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "POST":  # Only for creating a new post.
        try:
            post_type_id = req["post_type_id"]
            post_owner_user_name = req["post_owner_user_name"]
            post_entries_dictionary_list = req["post_entries_dictionary_list"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST

        else:
            try:
                new_post = Post.create_post(post_type_id, post_owner_user_name, post_entries_dictionary_list)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data["response_message"] = "Post is successfully created. "
                data["data"] = {"_id": new_post.get_id()}
                status_code = SC_SUCCESS

    elif request.method == "PUT":  # Only for creating a new post.

        try:
            _id = req["post_id"]
            post_entries_dictionary_list = req["post_entries_dictionary_list"]

        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST
        else:
            try:
                updated_post = Post.update_post(_id, post_entries_dictionary_list)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data["response_message"] = "Post is successfully updated. "
                data["data"] = {"_id": updated_post.get_id()}
                status_code = SC_SUCCESS

    elif request.method == "GET":
        try:
            post_id = req["post_id"]
        except Exception:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST
        else:
            try:
                post = Post.get_post(post_id)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data["response_message"] = "Post is successfully returned. "
                data["data"] = post.to_dict()
                status_code = SC_SUCCESS

    return data, status_code


@app.route('/api/post/like/', methods=['PUT'])
def post_like():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "PUT":
        try:
            post_id = req["post_id"]
            user_name = req["user_name"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST

        else:
            try:
                post = Post.get_post(post_id)
                post_liked_user_list = post.like(user_name)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data["response_message"] = "Post is successfully created. "
                data["data"] = {"post_liked_user_list": post_liked_user_list}
                status_code = SC_SUCCESS

    return data, status_code


@app.route('/api/post/unlike/', methods=['PUT'])
def post_unlike():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "PUT":
        try:
            post_id = req["post_id"]
            user_name = req["user_name"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST

        else:
            try:
                post = Post.get_post(post_id)
                post_liked_user_list = post.unlike(user_name)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data["response_message"] = "Post is successfully created. "
                data["data"] = {"post_liked_user_list": post_liked_user_list}
                status_code = SC_SUCCESS

    return data, status_code


@app.route('/api/post/participate/', methods=['PUT'])
def post_participate():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "PUT":
        try:
            post_id = req["post_id"]
            user_name = req["user_name"]
            header_of_participation_field = req["header_of_participation_field"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST

        else:
            try:
                post = Post.get_post(post_id)
                list_of_participants = post.participate_to_a_participation_field(header_of_participation_field,
                                                                                 user_name)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data[
                    "response_message"] = f"User with user_name: \"{user_name}\"has been successfully \
                     marked as participating to the \"Participation\" \
                     field with header: \"{header_of_participation_field}\""
                data["data"] = {"list_of_participants": list_of_participants}
                status_code = SC_SUCCESS

    return data, status_code


@app.route('/api/post/cancel_participation/', methods=['PUT'])
def post_cancel_participate():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "PUT":
        try:
            post_id = req["post_id"]
            user_name = req["user_name"]
            header_of_participation_field = req["header_of_participation_field"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST

        else:
            try:
                post = Post.get_post(post_id)
                list_of_participants = post.cancel_participation_to_a_participation_field(header_of_participation_field,
                                                                                          user_name)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data[
                    "response_message"] = f"User with user_name: \"{user_name}\" has been successfully \
                     unmarked as participating to the \"Participation\" \
                     field with header: \"{header_of_participation_field}\""
                data["data"] = {"list_of_participants": list_of_participants}
                status_code = SC_SUCCESS

    return data, status_code


@app.route('/api/post/vote/', methods=['PUT'])
def post_vote():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "PUT":
        try:
            post_id = req["post_id"]
            user_name = req["user_name"]
            header_of_poll_field = req["header_of_poll_field"]
            option = req["option"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST

        else:
            try:
                post = Post.get_post(post_id)
                options = post.vote_in_a_poll_field(header_of_poll_field,
                                                    option,
                                                    user_name)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data[
                    "response_message"] = f"User with user_name: \"{user_name}\" has been successfully \
                     voted for the option: \"{option}\" in the \"Poll\" \
                     field with header: \"{header_of_poll_field}\""
                data["data"] = {"options": options}
                status_code = SC_SUCCESS

    return data, status_code


@app.route('/api/post/cancel_vote/', methods=['PUT'])
def post_cancel_vote():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "PUT":
        try:
            post_id = req["post_id"]
            user_name = req["user_name"]
            header_of_poll_field = req["header_of_poll_field"]
            option = req["option"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST

        else:
            try:
                post = Post.get_post(post_id)
                options = post.cancel_vote_in_a_poll_field(header_of_poll_field,
                                                           option,
                                                           user_name)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data[
                    "response_message"] = f"User with user_name: \"{user_name}\" has successfully \
                         unvoted for the option: \"{option}\" in the \"Poll\" \
                         field with header: \"{header_of_poll_field}\""
                data["data"] = {"options": options}
                status_code = SC_SUCCESS

    return data, status_code


@app.route('/api/post_type/', methods=['GET', 'POST'])
def post_type():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "POST":  # Cannot edit post type, so this is creating a post type
        try:
            post_type_name = req["post_type_name"]
            parent_community_id = req["parent_community_id"]
            post_field_info_dictionaries_list = req["post_field_info_dictionaries_list"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST
        else:

            try:
                new_post_type = PostType.create_post_type(post_type_name,
                                                          parent_community_id,
                                                          post_field_info_dictionaries_list)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data["response_message"] = "PostType is successfully created."
                data["data"] = {"_id": new_post_type.get_id()}
                status_code = SC_SUCCESS

    elif request.method == "GET":
        try:
            _id = req["post_type_id"]
        except Exception as e:
            data = {"response_message": "Necessary arguments are not given."}
            status_code = SC_BAD_REQUEST
        else:

            try:
                new_post_type = PostType.get_post_type(_id)
            except Exception as e:
                data = {"response_message": str(e)}
                status_code = SC_BAD_REQUEST
            else:
                data["response_message"] = "PostType is successfully created."
                data["data"] = new_post_type.to_dict()
                status_code = SC_SUCCESS

    return data, status_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
