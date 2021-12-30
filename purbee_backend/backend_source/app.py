from flask import Flask, request
import re
from community.community import Community
from datetime import datetime as dt
import mpu
from collections import Counter

from database.database_utilities import (
    get_next_post_id,
    get_next_post_type_id,
    check_user_by_user_name,
    get_user_by_name,
    get_all_user_names,
    get_all_community_names
)
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


@app.route('/api/advanced_search', methods=['GET'])
def advanced_search():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    try:
        user_name = req["user_name"]
        search_dictionary = req["search_dictionary"]
        community_id = req["community_id"]
    except:
        data[
            'response_message'] = "Incorrect json content. (necessary field is search_dictionary,user_name,community_id)"
        status_code = SC_BAD_REQUEST
        return data, status_code

    if check_user_by_user_name(user_name):
        data['response_message'] = "there is no such user."
        status_code = SC_FORBIDDEN
        return data, status_code

    community = Community.get_community_from_id(community_id)

    if community.is_private:
        if user_name not in community.subscriber_list:
            data[
                'response_message'] = "this is a private community and this user is not a subscriber of this community"
            status_code = SC_FORBIDDEN
            return data, status_code

    # defaultCurrency is TL
    # default radius = 10 km
    # search dictionary = {"PlainText": "search_text", "Location" : {"longitude":"coordinates" , "latitude": "coordinates" , "radius":kms} ,
    # "DateTime" : {"starting_date": "date1" , "ending_date":"date2", "starting_time": "time1" , "ending_time":"time2"}, "Price" : {"min_price" : "price1", "max_price": "price2", "currency":"currency"},
    # "Participation" : {"min_participation" : min_participation , "max_participation" : max_participation}
    # }

    community_post_list = [Post.get_post_from_id(id) for id in community.subscriber_list]
    eligableList = []
    for filter in search_dictionary.keys():
        for post in community_post_list:
            for field in post.post_fields_list:
                if filter == "PlainText":
                    if type(field).__name__ == "PlainText":
                        search_text = search_dictionary["PlainText"]["search_text"]
                        if search_text in field.text:
                            eligableList.append(post._id)
                if filter == "DateTime":
                    if type(field).__name__ == "DateTime":
                        try:
                            starting_date = search_dictionary["DateTime"]["starting_date"]
                        except:
                            starting_date = "01.01.1000"

                        try:
                            ending_date = search_dictionary["DateTime"]["ending_date"]
                        except:
                            ending_date = "01.01.9999"

                        try:
                            starting_time = search_dictionary["DateTime"]["starting_time"]
                        except:
                            starting_time = "00.00"

                        try:
                            ending_time = search_dictionary["DateTime"]["ending_time"]
                        except:
                            ending_time = "23.59"

                        starting_date_converted = dt.strptime(starting_date, "%d/%m/%y")
                        ending_date_converted = dt.strptime(ending_date, "%d/%m/%y")
                        starting_time_converted = dt.strptime(starting_time, '%H:%M')
                        ending_time_converted = dt.strptime(ending_time, '%H:%M')

                        if ending_date_converted >= field.date >= starting_date_converted:
                            if ending_time_converted >= field.time >= starting_time_converted:
                                eligableList.append(post._id)
                if filter == "Price":
                    if type(field).__name__ == "Price":
                        try:
                            min_price = float(search_dictionary["Price"]["min_price"])
                        except:
                            min_price = 0

                        try:
                            max_price = float(search_dictionary["Price"]["max_price"])
                        except:
                            max_price = 999999999

                        try:
                            currency = search_dictionary["Price"]["currency"]
                        except:
                            currency = "TL"

                        if max_price >= field.amount >= min_price:
                            if field.currency == currency:
                                eligableList.append(post._id)

                if filter == "Participation":
                    if type(field).__name__ == "Participation":
                        try:
                            min_participation = int(search_dictionary["Participation"]["min_participation"])
                        except:
                            min_participation = 0

                        try:
                            max_participation = search_dictionary["Participation"]["max_participation"]
                        except:
                            max_participation = 999999999

                        if max_participation >= len(field.list_of_participants)  >= min_participation:
                            eligableList.append(post._id)

                if filter == "Location":
                    if type(field).__name__ == "Location":
                        lat1 = search_dictionary["Location"]["latitude"]
                        lon1 = search_dictionary["Location"]["longitude"]
                        lat2 = field.latitude
                        lon2 = field.longitude

                        try:
                            radius = search_dictionary["Location"]["radius"]
                        except:
                            data['response_message'] = "radius value needed for location filter"
                            status_code = SC_BAD_REQUEST
                            return data, status_code

                        dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))

                        if dist <= float(radius):
                            eligableList.append(post._id)

    occurences = Counter(eligableList)
    results = [el for el in occurences.keys() if occurences[el] >= len(search_dictionary.keys())]
    data['response_message'] = "search result successfully returned"
    data['post_ids'] = results
    status_code = SC_SUCCESS
    return data, status_code


@app.route('/api/user_search', methods=['GET'])
def user_search():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    try:
        search_text = req["search_text"]
    except:
        data['response_message'] = "Incorrect json content. (necessary field is search_text)"
        status_code = SC_BAD_REQUEST
        return data, status_code

    user_names = get_all_user_names()

    user_names_contains_given_text = [el for el in user_names if search_text in el]

    data['response_message'] = "search result successfully returned"
    data['user_names'] = user_names_contains_given_text
    status_code = SC_SUCCESS
    return data, status_code


@app.route('/api/community_search', methods=['GET'])
def community_search():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    try:
        search_text = req["search_text"]
    except:
        data['response_message'] = "Incorrect json content. (necessary field is search_text)"
        status_code = SC_BAD_REQUEST
        return data, status_code

    community_names = get_all_community_names()

    community_names_contains_given_text = [el for el in community_names if search_text in str(el)]

    data['response_message'] = "search result successfully returned"
    data['community_names'] = community_names_contains_given_text
    status_code = SC_SUCCESS
    return data, status_code


@app.route('/api/user_feed', methods=['GET'])
def user_feed():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    try:
        user_name = req["user_name"]
    except:
        data['response_message'] = "Incorrect json content. (necessary field is user_name)"
        status_code = SC_BAD_REQUEST
        return data, status_code

    if check_user_by_user_name(user_name):
        data['response_message'] = "there is no such user."
        status_code = SC_FORBIDDEN
        return data, status_code

    post_list = {}
    user = get_user_by_name(user_name)
    following_list = user["following"]
    for followedUserName in following_list:
        followedUser = get_user_by_name(followedUserName)
        followedUserPostList = followedUser["post_list"]
        for postId in followedUserPostList:
            post = Post.get_post_from_id(postId)
            parent_community_id = post["base_post_type"]["parent_community_id"]
            community = Community.get_community_from_id(parent_community_id)
            if user_name not in community.subscriber_list:
                if community.is_private:
                    continue

            post_list[postId] = post["date"]

    for communityId in user["subscribed_communities"]:
        community = Community.get_community_from_id(communityId)
        for postId in community["post_history_id_list"]:
            post = Post.get_post_from_id(postId)
            post_list[postId] = post["date"]

    post_list = list(dict.fromkeys(post_list))

    dict(sorted(post_list.items(), key=lambda item: item[1], reverse=True))

    data['response_message'] = "user feed post list successfully returned"
    data['user_feed_post_list'] = post_list
    status_code = SC_SUCCESS
    return data, status_code


@app.route('/api/community_page/admin', methods=['PUT'])
def community_page_admin():
    req = request.get_json()
    data = {'response_message': None}
    status_code = None
    if request.method == "PUT":
        needed_keys = ['admin_id', 'user_id', 'community_id', 'action']
        if len(needed_keys) != len(req):
            data[
                'response_message'] = "Incorrect json content. (needed keys are admin_id, user_id, community_id, action)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                data[
                    'response_message'] = "Incorrect json content. (needed keys are admin_id, user_id, community_id, action)"
                status_code = SC_BAD_REQUEST
                return data, status_code

        result, current_community = Community.make_or_remove_admin(req['admin_id'], req['community_id'], req['user_id'],
                                                                   req['action'])

        if result == 0:
            # successful
            data['response_message'] = "Registered user successfully changed"
            data['community'] = current_community
            status_code = SC_SUCCESS
        elif result == 1:
            # internal error
            data['response_message'] = "Some internal error occurred"
            status_code = SC_INTERNAL_ERROR
        elif result == 2:
            # bad request
            data[
                'response_message'] = "Incorrect json content. (needed keys are admin_id, user_id, community_id, action)"
            status_code = SC_BAD_REQUEST
        elif result == 11:
            data['response_message'] = "There is no community with the given community id"
            status_code = SC_FORBIDDEN
        elif result == 12:
            data['response_message'] = "There is no registered user with the given user id"
            status_code = SC_FORBIDDEN
        elif result == 13:
            data['response_message'] = "There is no registered user with the given admin id"
            status_code = SC_FORBIDDEN
        elif result == 14:
            data['response_message'] = "Registered user with the admin id is not an admin or community creator"
            status_code = SC_FORBIDDEN
        elif result == 15:
            data['response_message'] = "Registered user with the user id is already an admin"
            status_code = SC_FORBIDDEN
        elif result == 16:
            data['response_message'] = "Registered user with the user id is not an admin"
            status_code = SC_FORBIDDEN

        return data, status_code


@app.route('/api/community_page/request', methods=['PUT'])
def handle_community_page_subscription_request():
    req = request.get_json()
    data = {'response_message': None}
    status_code = None
    if request.method == "PUT":
        needed_keys = ['admin_id', 'user_id', 'community_id', 'action']
        if len(needed_keys) != len(req):
            data[
                'response_message'] = "Incorrect json content. (needed keys are admin_id, user_id, community_id, action)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                data[
                    'response_message'] = "Incorrect json content. (needed keys are admin_id, user_id, community_id, action)"
                status_code = SC_BAD_REQUEST
                return data, status_code
        result, current_community = Community.accept_or_reject_subscription_requester(req['admin_id'],
                                                                                      req['community_id'],
                                                                                      req['user_id'], req['action'])

        if result == 0:
            # successful
            data['response_message'] = "Requester successfully {}ed".format(req['action'])
            data['community'] = current_community
            status_code = SC_SUCCESS
        elif result == 1:
            # internal error
            data['response_message'] = "Some internal error occurred"
            status_code = SC_INTERNAL_ERROR
        elif result == 2:
            # bad request
            data[
                'response_message'] = "Incorrect json content. (needed keys are admin_id, user_id, community_id, action)"
            status_code = SC_BAD_REQUEST
        elif result == 11:
            data['response_message'] = "There is no community with the given community id"
            status_code = SC_FORBIDDEN
        elif result == 12:
            data['response_message'] = "There is no registered user with the given user id"
            status_code = SC_FORBIDDEN
        elif result == 13:
            data['response_message'] = "There is no registered user with the given admin id"
            status_code = SC_FORBIDDEN
        elif result == 14:
            data['response_message'] = "Registered user with the admin id is not an admin"
            status_code = SC_FORBIDDEN
        elif result == 15:
            data['response_message'] = "Registered user with the user id is not a subscription requester"
            status_code = SC_FORBIDDEN
        elif result == 16:
            data['response_message'] = "Registered user with the user id is already a subscriber"
            status_code = SC_FORBIDDEN

        return data, status_code


@app.route('/api/community_page/ban', methods=["PUT"])
def ban_from_community_page():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    if request.method == "PUT":
        needed_keys = ['admin_id', 'community_id', 'user_id']
        if len(needed_keys) != len(req):
            # return invalid input error
            data['response_message'] = "Incorrect json content. (necessary fields are admin_id, community_id, user_id)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                data[
                    'response_message'] = "Incorrect json content. (necessary fields are admin_id, community_id, user_id)"
                status_code = SC_BAD_REQUEST
                return data, status_code

        result, current_community = Community.ban_user(req['admin_id'], req['community_id'], req['user_id'])

        if result == 0:
            # success
            data['response_message'] = "Given user successfully banned"
            data['community'] = current_community
            status_code = SC_SUCCESS
        elif result == 1:
            # internal error
            data['response_message'] = "Some internal error occurred"
            status_code = SC_INTERNAL_ERROR
        elif result == 2:
            # user is already banned
            data['response_message'] = "Given user with the user_id is already banned"
            status_code = SC_FORBIDDEN
        elif result == 11:
            data['response_message'] = "There is no community with the given community_id"
            status_code = SC_FORBIDDEN
        elif result == 12:
            data['response_message'] = "There is no user with the given user_id"
            status_code = SC_FORBIDDEN
        elif result == 13:
            data['response_message'] = "There is no user with the given admin_id"
            status_code = SC_FORBIDDEN
        elif result == 14:
            data['response_message'] = "The given user with the admin_id is not an admin"
            status_code = SC_FORBIDDEN
        elif result == 15:
            data['response_message'] = "The given user with the user_id is an admin"
            status_code = SC_FORBIDDEN
        elif result == 16:
            data['response_message'] = "The given user with the user_id is the community creator"
            status_code = SC_FORBIDDEN

        return data, status_code


@app.route('/api/community_page/unban', methods=["PUT"])
def unban_from_community_page():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    if request.method == "PUT":
        needed_keys = ['admin_id', 'community_id', 'user_id']
        if len(needed_keys) != len(req):
            # return invalid input error
            data['response_message'] = "Incorrect json content. (necessary fields are admin_id, community_id, user_id)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                data[
                    'response_message'] = "Incorrect json content. (necessary fields are admin_id, community_id, user_id)"
                status_code = SC_BAD_REQUEST
                return data, status_code

        result, current_community = Community.unban_user(req['admin_id'], req['community_id'], req['user_id'])

        if result == 0:
            # success
            data['response_message'] = "Given user successfully unbanned"
            data['community'] = current_community
            status_code = SC_SUCCESS
        elif result == 1:
            # internal error
            data['response_message'] = "Some internal error occurred"
            status_code = SC_INTERNAL_ERROR
        elif result == 11:
            data['response_message'] = "There is no community with the given community_id"
            status_code = SC_FORBIDDEN
        elif result == 12:
            data['response_message'] = "There is no user with the given user_id"
            status_code = SC_FORBIDDEN
        elif result == 13:
            data['response_message'] = "There is no user with the given admin_id"
            status_code = SC_FORBIDDEN
        elif result == 14:
            data['response_message'] = "The given user with the admin_id is not an admin"
            status_code = SC_FORBIDDEN
        elif result == 15:
            data['response_message'] = "The given user with the user_id is not a banned user"
            status_code = SC_FORBIDDEN
        return data, status_code


@app.route('/api/community_page/change_privacy', methods=["PUT"])
def change_privacy_community_page():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    if request.method == "PUT":
        needed_keys = ['community_id', 'admin_id']
        if len(needed_keys) != len(req):
            # return invalid input error
            data['response_message'] = "Incorrect json content. (necessary fields are admin_id and community_id)"

            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                data['response_message'] = "Incorrect json content. (necessary fields are admin_id and community_id)"
                status_code = SC_BAD_REQUEST

        result, current_community = Community.change_privacy(req['admin_id'], req['community_id'])

        if result == 0:
            # successful make private
            data['response_message'] = "Community privacy set to private"
            data['community'] = current_community
            status_code = SC_SUCCESS
        elif result == 10:
            # successful make public
            data['response_message'] = "Community privacy set to public"
            data['community'] = current_community
            status_code = SC_SUCCESS
        elif result == 11:
            data['response_message'] = "There is no community with the given community id {}".format(
                req['community_id'])
            status_code = SC_FORBIDDEN
        elif result == 12:
            data['response_message'] = "There is no user with the given registered user id {}".format(req['admin_id'])
            status_code = SC_FORBIDDEN
        elif result == 13:
            data['response_message'] = "The user with the given id {} is not an admin of the community {}".format(
                req['admin_id'], req['community_id'])
            status_code = SC_FORBIDDEN
        elif result == 1:
            data['response_message'] = "Some internal error occurred"
            status_code = SC_INTERNAL_ERROR
        return data, status_code


@app.route('/api/community_feed', methods=['GET'])
def community_feed():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    needed_keys = ["user_name", "community_id"]
    if 2 != len(req):
        # return invalid input error
        data['response_message'] = "Incorrect json content. (necessary fields are user_name, community_id)"
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

    community_id = req["community_id"]
    user_name = req["user_name"]

    if check_user_by_user_name(user_name):
        data['response_message'] = "there is no such user."
        status_code = SC_FORBIDDEN
        return data, status_code

    community = Community.get_community_from_id(community_id)

    if user_name not in community.subscriber_list:
        if community.is_private:
            data['response_message'] = "this is a private community and the user is not a subscriber of this community."
            status_code = SC_FORBIDDEN
            return data, status_code

    if not community:
        data['response_message'] = "there is no such community."
        status_code = SC_FORBIDDEN
        return data, status_code

    data['response_message'] = "community post list successfully returned"
    data['community_post_list'] = community.post_history_id_list.reverse()
    status_code = SC_SUCCESS
    return data, status_code


@app.route('/api/community_page/subscribe', methods=["PUT"])
def subscribe_to_community_page():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None
    if request.method == "PUT":
        needed_keys = ['user_id', 'community_id']
        if len(needed_keys) != len(req):
            # return invalid input error
            data['response_message'] = "Incorrect son content. (necessary fields are user_id and community_id)"
            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                data['response_message'] = "Incorrect son content. (necessary fields are user_id and community_id)"
                status_code = SC_BAD_REQUEST
                return data, status_code

        result, current_community = Community.subscribe(req['user_id'], req['community_id'])

        if result == 0:
            # successful
            data['response_message'] = "Registered user with the id {} successfully subscribed to Community with " \
                                       "the id {}".format(req['user_id'], req['community_id'])
            data['community'] = current_community
            status_code = SC_SUCCESS
            return data, status_code
        elif result == 1:
            # update failed
            data['response_message'] = "Some internal error occured"
            status_code = SC_INTERNAL_ERROR
            return data, status_code
        elif result == 2:
            # user is already subscriber
            data['response_message'] = "Registered user with the id {} is already subscriber or requester".format(
                req['user_id'])
            status_code = SC_FORBIDDEN
            return data, status_code
        elif result == 11:
            # there is no community
            data['response_message'] = "There is no community with the id {}".format(req['community_id'])
            status_code = SC_FORBIDDEN
            return data, status_code
        elif result == 12:
            data['response_message'] = "There is no registered user with the id {}".format(req['user_id'])
            status_code = SC_FORBIDDEN
            # there is no user
            return data, status_code
        elif result == 10:
            data['response_message'] = "Registered user {} added to the requester list".format(req['user_id'])
            data['community'] = current_community
            status_code = SC_SUCCESS
            return data, status_code


@app.route('/api/community_page/unsubscribe', methods=["PUT"])
def unsubscribe_from_community_page():
    req = request.get_json()
    data = {'response_message': None}
    status_code = None
    if request.method == "PUT":
        needed_keys = ['user_id', 'community_id']
        if len(needed_keys) != len(req):
            # return invalid input error
            data['response_message'] = "Incorrect json content. (necessary fields are user_id and community_id)"

            status_code = SC_BAD_REQUEST
            return data, status_code
        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                data[
                    'response_message'] = "Incorrect json content. (necessary fields are user_id and community_id)"
                status_code = SC_BAD_REQUEST
                return data, status_code

        for r_keys in req:
            if r_keys in needed_keys:
                pass
            else:
                # return invalid input error
                pass

    result, current_community = Community.unsubscribe(req['user_id'], req['community_id'])

    if result == 0:
        # successfully removed subscription from private or non private community
        data['response_message'] = "Registered user with the id {} successfully unsubscribed".format(req['user_id'])
        data['community'] = current_community
        status_code = SC_CREATED
        return data, status_code
    elif result == 10:
        # successfully removed request from private community
        data['response_message'] = "Registered user with the id {} successfully removed subscription request".format(
            req['user_id'])
        data['community'] = current_community
        status_code = SC_CREATED
        return data, status_code
    elif result == 1:
        # update failed
        data['response_message'] = "Some internal error occured"
        status_code = SC_INTERNAL_ERROR
        return data, status_code
    elif result == 2:
        # user is not subscriber or requester
        data['response_message'] = "Registered user with the id {} is not subscriber or subscription requester of the " \
                                   "community with the id {}".format(req['user_id'], req['community_id'])
        status_code = SC_FORBIDDEN
        return data, status_code
    elif result == 11:
        # there is no community
        data['response_message'] = "There is no community with the id {}".format(req['community_id'])
        status_code = SC_FORBIDDEN
        return data, status_code
    elif result == 10:
        # there is no user
        data['response_message'] = "There is no registered user with the id {}".format(req['user_id'])
        status_code = SC_FORBIDDEN
        return data, status_code


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
        post_type_id = req["post_type_id"]
        fields_dictionary = req["fields_dictionary"]
        post_id = get_next_post_id()
        user_name = req["user_name"]  # TODO: use for authorization

        base_post_type = PostType.get_post_type_from_id(post_type_id)
        for key in fields_dictionary.keys():
            field_dics = fields_dictionary[key]
            actual_name = "_".join([i.lower() for i in re.findall('[A-Z][^A-Z]*', key)]) + "_fields"
            w_header_field_dics = getattr(base_post_type.post_fields, actual_name)
            for field_dic, w_header in zip(field_dics, w_header_field_dics):
                field_dic["header"] = w_header.header
        try:
            post = Post(base_post_type, fields_dictionary, post_id, user_name)
        except Exception as e:
            if str(e) == "All fields should be specified":
                data["response_message"] = str(e)
                status_code = SC_BAD_REQUEST
            print(str(e))
            # TODO: Add other cases for other possible exceptions
            return data, status_code

        print("the post:", post.to_dict())
        post.save2database()  # TODO: check for database errors
        post.has_created()

        post_id = post.post_id
        del post

        # TODO: check_if_eligible(user_name,parent_community_id)

        return_status = 0
        if return_status == 0:
            data["response_message"] = "Post is successfully created. "
            data["data"] = {"post_id": post_id}
            status_code = SC_SUCCESS
        elif return_status == 1:
            data["response_message"] = "Some error occurred"
            status_code = SC_BAD_REQUEST

    elif request.method == "PUT":  # Only for creating a new post.
        post_id = req["post_id"]
        fields_dictionary = req["fields_dictionary"]
        user_name = req["user_name"]  # TODO: use for authorization

        post = Post.get_post_from_id(post_id)
        try:
            updated_post = post.update(post.base_post_type, fields_dictionary, post.id, post.owner_user_name)
        except Exception as e:
            if str(e) == "All fields should be specified":
                data["response_message"] = str(e)
                status_code = SC_BAD_REQUEST
            # TODO: Add other cases for other possible exceptions
            return data, status_code

        updated_post.save2database()  # TODO: check for database errors

        post_id = updated_post.id
        del updated_post

        # TODO: check_if_eligible(user_name,parent_community_id)

        return_status = 0
        if return_status == 0:
            data["response_message"] = "Post is successfully created. "
            data["data"] = {"post_id": post_id}
            status_code = SC_SUCCESS
        elif return_status == 1:
            data["response_message"] = "Some error occurred"
            status_code = SC_BAD_REQUEST

    elif request.method == "GET":
        post_id = req["post_id"]
        user_name = req["user_name"]  # TODO: use for authorization

        post = Post.get_post_from_id(post_id)

        # TODO: check_if_eligible(user_name,parent_community_id)

        return_status = 0
        if return_status == 0:
            data["response_message"] = "Post is successfully created. "
            data["data"] = post.to_dict()
            status_code = SC_SUCCESS
        elif return_status == 1:
            data["response_message"] = "Some error occurred"
            status_code = SC_BAD_REQUEST

    return data, status_code


@app.route('/api/post_type/', methods=['GET', 'POST'])
def post_type():
    req = request.get_json()
    data = {"response_message": None}
    status_code = None

    if request.method == "POST":  # Cannot edit post type, so this is creating a post type
        fields_dictionary = req["fields_dictionary"]
        user_name = req["user_name"]  # TODO: use for authorization
        post_type_name = req["post_type_name"]
        parent_community_id = req["parent_community_id"]

        community = Community.get_community_from_id(parent_community_id)  # TODO: use for authorization

        post_type_id = get_next_post_type_id()
        post_type = PostType(fields_dictionary, post_type_name, parent_community_id, post_type_id)

        post_type.save2database()
        post_type.has_created()

        post_type_id = post_type.post_type_id
        del post_type

        # TODO: check_if_eligible(user_name,parent_community_id)

        return_status = 0
        if return_status == 0:
            data["response_message"] = "PostType is successfully created."
            data["data"] = {"post_type_id": post_type_id}
            status_code = SC_SUCCESS
        elif return_status == 1:
            data["response_message"] = "Some error occurred"
            status_code = SC_BAD_REQUEST

    elif request.method == "GET":
        post_type_id = req["post_type_id"]

        post_type = PostType.get_post_type_from_id(post_type_id)

        post_type_dict = post_type.to_dict()

        return_status = 0
        if return_status == 0:
            data["response_message"] = "PostType is successfully returned."
            data["data"] = post_type_dict
            status_code = SC_SUCCESS
        elif return_status == 1:
            data["response_message"] = "Some error occurred"
            status_code = SC_BAD_REQUEST

        del post_type

    return data, status_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
