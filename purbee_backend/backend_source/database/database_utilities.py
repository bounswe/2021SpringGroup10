import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://purbeeApp:QLi9WWoLf4MztDJv@cluster0.orh8z.mongodb.net/purbeeProduct?retryWrites=true&w=majority")
db = client.purbeeProduct
registered_users = db["registered_users"]
post_types = db["PostTypes"]
posts = db["Posts"]
nextIds = db["nextIds"]
communities = db['communities']
discussions = db['discussions']
comments = db['comments']

test_db = client.purbeeTest
test_registered_users = test_db["registered_users"]
test_post_types = test_db["post_types"]
test_posts = test_db["posts"]
test_nextIds = test_db['nextIds']
test_communities = test_db['communities']
test_discussions = test_db['discussions']
test_comments = test_db['comments']

def get_community_by_community_id(community_id, env=None):
    if env == "test":
        community_database = test_communities
    else:
        community_database = communities
    return community_database.find_one({"_id": community_id})


def get_all_community_names():
    return [community["_id"] for community in communities.find({})]


def get_all_user_names():
    return [user["user_name"] for user in registered_users.find({})]


def update_community(community_dictionary, env=None):
    if env == "test":
        community_database = test_communities
    else:
        community_database = communities
    db_return = community_database.update({"_id": community_dictionary['_id']}, {
        "$set": community_dictionary})


    if db_return["ok"] != 1.0:
        return 1
    else:
        return 0


def create_new_comment(comment_dict, env=None):
    if env == "test":
        comment_db = test_comments
    else:
        comment_db = comments
    if get_comment_dict_by_comment_id(comment_dict["id"], env):
        return 1
    try:
        neu_comment = {}
        for key in comment_dict:
            if key == "id":
                neu_comment['_id'] = comment_dict[key]
            else:
                neu_comment[key] = comment_dict[key]

        comment_db.insert_one(neu_comment)
        return 0
    except:
        return 2


def get_comment_dict_by_comment_id(comment_id, env=None):
    if env == 'test':
        comment_db = test_comments
    else:
        comment_db = comments
    return comment_db.find_one({"_id": comment_id})


def update_comment(comment_dictionary, env=None):
    if env == 'test':
        comment_db = test_comments
    else:
        comment_db = comments
    id_value = comment_dictionary.pop('id')
    db_return = comment_db.update({"_id": id_value}, {
        "$set": comment_dictionary
    })

    if db_return["ok"] != 1.0:
        return 1
    else:
        return 0


def update_discussion(discussion_dictionary, env=None):
    if env == 'test':
        discussion_db = test_discussions
    else:
        discussion_db = discussions
    id_value = discussion_dictionary.pop('id')
    db_return = discussion_db.update({"_id": id_value}, {
        "$set": discussion_dictionary
    })

    if db_return["ok"] != 1.0:
        return 1
    else:
        return 0


def create_new_discussion(discussion_dictionary, env=None):
    if env == 'test':
        discussion_db = test_discussions
    else:
        discussion_db = discussions
    if get_discussion_dict_by_discussion_id(discussion_dictionary["id"], env):
        return 1
    try:
        neu_discussion = {}
        for key in discussion_dictionary:
            if key == "id":
                neu_discussion['_id'] = discussion_dictionary[key]
            else:
                neu_discussion[key] = discussion_dictionary[key]

        discussion_db.insert_one(neu_discussion)
        return 0
    except:
        return 2


def get_discussion_dict_by_discussion_id(discussion_id, env=None):
    if env == "test":
        discussion_db = test_discussions
    else:
        discussion_db = discussions
    return discussion_db.find_one({"_id": discussion_id})


def save_new_community(community_dictionary, env=None):
    # RETURN
    # 0 -> Success
    # 1 -> already have this community with community id
    # 2 -> some another error probably related with community_dictionary
    if env == "test":
        community_database = test_communities
    else:
        community_database = communities
    if get_community_by_community_id(community_dictionary['id'], env):
        return 1
    try:
        community = {}
        for key in community_dictionary:
            if key == 'id':
                community['_id'] = community_dictionary[key]

            community[key] = community_dictionary[key]

        community_database.insert_one(community)
        return 0
    except:
        return 2


def add_post_to_user_postlist(user_name, post_id):
    post_list = get_user_by_name(user_name)["post_list"]
    post_list.append(post_id)
    registered_users.update({"user_name": user_name}, {"$set": {"post_list": post_list}})


def remove_post_from_user_postlist(user_name, post_id):
    post_list = get_user_by_name(user_name)["post_list"]
    post_list.pop(post_id)
    registered_users.update({"user_name": user_name}, {"$set": {"post_list": post_list}})


def save_post(post_dict):
    info = posts.insert_one(post_dict)
    return info.inserted_id


def update_post(post_dict):
    info = posts.update({"_id": post_dict["_id"]}, {"$set": post_dict})
    return info["nModified"]


def get_post(post_id: int):
    res = posts.find_one({"_id": post_id})
    return res


def delete_post(post_id: int):
    info = posts.delete_one({"_id": post_id})
    return info.deleted_count


def save_post_type(post_type_dict):
    info = post_types.insert_one(
        post_type_dict)  # returns WriteResult object
    return info.inserted_id


def update_post_type(post_dict):
    info = post_types.update({"_id": post_dict["_id"]}, {"$set": post_dict})
    return info["nModified"]


def get_post_type(post_type_id):
    res = post_types.find_one(
        {"_id": post_type_id})  # returns dict where value of "_id" is <bson ObjectId obj>
    return res


def delete_post_type(post_type_id: int):
    info = posts.delete_one({"_id": post_type_id})  # returns DeleteResult object
    return info.deleted_count


# community id decided by the user and does not related with any
# database operations. So that, I, @OnurSefa, believe that this
# functionality is unnecessary and irrelevant
# def get_next_community_id():
# pass

def get_user_by_name(user_name, env=None):
    """
    :param
        user_name:
    :return:
        None if fails to find the user. Else returns user dictionary.
    """
    if env == "test":
        registered_user_database = test_registered_users
    else:
        registered_user_database = registered_users
    return registered_user_database.find_one({"user_name": user_name})


def check_user_by_user_name(user_name):
    if registered_users.find_one({"user_name": user_name}) is None:
        return 1
    else:
        return 0


def save_new_user(user_name, mail_address, password):
    if get_user_by_mail_address(mail_address):
        return 2
    try:
        user = {"_id": user_name, "user_name": user_name, "mail_address": mail_address, "password": password,
                "followers": [], "following": [], "profile_photo": [], "last_name": [], "first_name": [],
                "birth_date": [], "post_list": [], "subscribed_communities": []}
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


def update_profile_info_by_user_name(user_name, profile_info_dict):
    db_return = registered_users.update({"user_name": user_name}, {
        "$set": profile_info_dict})

    if db_return["ok"] != 1.0:
        return 1
    else:
        return 0


# 0 for successful update, 1 for error during database operation
def update_follower_and_following_lists(user_name1, user_name2):
    try:
        following = get_user_by_name(user_name1)["following"]
        following.append(user_name2)
        registered_users.update({"user_name": user_name1}, {"$set": {"following": following}})
        followers = get_user_by_name(user_name2)["followers"]
        followers.append(user_name1)
        registered_users.update({"user_name": user_name2}, {"$set": {"followers": followers}})
        return 0
    except:
        return 1

def update_follower_and_following_lists2(user_name1, user_name2):
    try:
        following = get_user_by_name(user_name1)["following"]
        following.remove(user_name2)
        registered_users.update({"user_name": user_name1}, {"$set": {"following": following}})
        followers = get_user_by_name(user_name2)["followers"]
        followers.remove(user_name1)
        registered_users.update({"user_name": user_name2}, {"$set": {"followers": followers}})
        return 0
    except:
        return 1

def update_user_subscribed_communities(username,community_id):
    subscribed_communities = get_user_by_name(username)["subscribed_communities"]
    subscribed_communities.append(community_id)
    registered_users.update({"user_name": username}, {"$set": {"subscribed_communities": subscribed_communities}})

def get_profile_page_by_user_name(user_name):
    user = get_user_by_name(user_name)
    if user is None:
        return 1
    else:
        profile_info_fields = ['profile_photo', "following", "followers", "first_name", "last_name", "birth_date",
                               "post_list", "user_name"]
        return {key: value for key, value in user.items() if (key in profile_info_fields)}
