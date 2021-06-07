import sys


def get_user(user_name, collection):
    x = collection.find_one({"name": user_name})
    value = {
        "name": user_name,
        "jokes": x["jokes"]
    }
    return value


def add_user(user_name, collection):
    x = collection.insert_one({"name": user_name, "jokes": []})
    return x


def add_to_list(user_name, set_up, punch_line, collection):
    user = collection.find_one({"name": user_name})
    user_jokes = user["jokes"]
    set_up = set_up.replace("_", "?")
    punch_line = punch_line.replace("_", "?")
    if len(user_jokes) <= 0:
        x = collection.update_one({"name": user_name}, {"$set": {'jokes': [{'set_up': set_up, 'punch_line': punch_line}]}})
    else:
        user_jokes.append({'set_up': set_up, 'punch_line': punch_line})
        x = collection.update_one({"name": user_name}, {"$set": {'jokes': user_jokes}})
    return x
