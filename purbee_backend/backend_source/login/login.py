from purbee_backend.backend_source.database.database_utilities import (
    user_name_exists,
    mail_address_exists,
    save_new_user_to_database,
    get_password_from_user_name
)

from login_utilities import (
    password_secure
)


def signup(user_name, mail_address, password):
    if user_name_exists(user_name):
        return -1
    if mail_address_exists(mail_address):
        return -2
    if not password_secure(password):
        return -3

    save_new_user_to_database(user_name, mail_address, password)

    return 0


def login(user_name, password):
    return password == get_password_from_user_name(user_name)



