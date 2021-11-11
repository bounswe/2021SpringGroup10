import pymongo

client = pymongo.MongoClient("mongodb+srv://purbee2:abcd@purbee.am5x7.mongodb.net/purbee?retryWrites=true&w=majority")
db = client.purbee
registered_Users = db["registered_users"]


def get_user_name(user_name):
    pass


def get_mail_address(user_name):
    pass


def save_new_user(user_name, mail_address, password):
    user = {"user_name" : user_name , "mail_address" : mail_address, "password" : password}
    return registered_Users.insert_one(user)


def check_password_for_user_name(user_name, password):
    if registered_Users.findOne({"user_name": user_name, "password": password}):
        return 1
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
