
def get_user(user_name, collection):
    x = collection.find_one({"name": user_name})
    return x


def save_user(user_name, token, collection):
    x = collection.insert_one({"name": user_name, "spotify_token": token})
    return x