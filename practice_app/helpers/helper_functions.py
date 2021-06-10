def joke_get_user(user_name, collection):
    x = collection.find_one({"name": user_name})
    value = {
        "name": user_name,
        "jokes": x["jokes"]
    }
    return value


def joke_add_user(user_name, collection):
    x = collection.insert_one({"name": user_name, "jokes": []})
    value = {
        "id": str(x.inserted_id)
    }
    return value, 201


def joke_add_to_list(user_name, set_up, punch_line, collection):
    user = collection.find_one({"name": user_name})
    user_jokes = user["jokes"]
    set_up = set_up.replace("_", "?")
    punch_line = punch_line.replace("_", "?")
    if len(user_jokes) <= 0:
        x = collection.update_one({"name": user_name}, {"$set": {'jokes': [{'set_up': set_up, 'punch_line': punch_line}]}})
    else:
        user_jokes.append({'set_up': set_up, 'punch_line': punch_line})
        x = collection.update_one({"name": user_name}, {"$set": {'jokes': user_jokes}})

    value = {
        "modified_count": x.modified_count,
    }
    return value


def joke_delete_user(user_name, collection):
    x = collection.delete_one({"name": user_name})
    value = {
        "deleted_count": x.deleted_count
    }
    return value

