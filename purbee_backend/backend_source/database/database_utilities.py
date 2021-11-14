import sys

import pymongo
import sys
client = pymongo.MongoClient("mongodb+srv://purbeeApp:QLi9WWoLf4MztDJv@cluster0.orh8z.mongodb.net/purbeeProduct?retryWrites=true&w=majority")
db = client.purbeeProduct
registered_users = db["registered_users"]


def get_user_name(user_name):
    pass


def get_mail_address(user_name):
    pass

def get_user_by_name(user_name):
    return registered_users.find_one({"user_name": user_name})

def check_user_by_user_name(user_name):
    try:
        registered_users.find_one({"user_name": user_name})
        return 0
    except:
        return 1


def save_new_user(user_name, mail_address, password):
    if get_user_by_mail_address(mail_address):
        return 2
    try:
        user = {"_id": user_name, "user_name": user_name, "mail_address": mail_address, "password": password, "followers": [], "following": [], "profile_photo": [], "last_name": [], "first_name":[], "birth_date":[], "post_list": []}
        registered_users.insert_one(user)
    except:
        return 1

    return 0


def check_password_for_user_name(user_name, password):
    if registered_users.find_one({"user_name": user_name, "password": password}):
        return 0
    else:
        return 1


def get_user_by_mail_address(mail_address):
    user = registered_users.find_one({"mail_address": mail_address})
    if user:
        return user
    else:
        return 0

def set_profile_picture_by_user_name(user_name, picture):
    pass


def get_profile_picture_by_user_name(user_name):
    pass


def set_first_name_by_user_name(user_name, first_name):
    pass


def get_first_name_by_user_name(user_name):
    pass


def set_last_name_by_user_name(user_name, last_name):
    pass


def get_last_name_by_user_name(user_name):
    pass


def set_birth_date_by_user_name(user_name, birth_date):
    pass


def get_birth_date_by_user_name(user_name):
    pass

def update_profile_info_by_user_name(user_name,profile_photo,bio,first_name,last_name,birth_date):
    try:
        registered_users.update({"user_name": user_name}, {"$set": {"profile_photo": profile_photo, "bio": bio, "first_name": first_name, "last_name": last_name, "birth_date": birth_date}})
        return 0
    except:
        return 1

# 0 for successful update, 1 for error during database operation
def update_follower_and_following_lists(user_name1,user_name2):
    try:
        following = get_user_by_name(user_name1)["following"]
        following.append(user_name2)
        registered_users.update({"user_name":user_name1},  {"$set":{"following":following}})
        followers = get_user_by_name(user_name2)["followers"]
        followers.append(user_name1)
        registered_users.update({"user_name": user_name2}, {"$set": {"followers": followers}})
        return 0
    except:
        return 1

def get_profile_page_by_user_name(user_name):
    try:
        user = get_user_by_name(user_name)
        return user['profile_photo'], user['following'], user['followers'], user['first_name'], user['last_name'], user['birth_date'], user['post_list']
    except:
        return None



