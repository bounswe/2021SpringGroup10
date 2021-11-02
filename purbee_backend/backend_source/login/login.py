from purbee_backend.backend_source.database.database_utilities import (
    get_user_name,
    get_mail_address,
    save_new_user,
    get_password_from_user_name
)

from login_utilities import (
    password_secure
)


def signup(user_name, mail_address, password):
    if get_user_name(user_name):
        return -1
    if get_mail_address(mail_address):
        return -2
    if not password_secure(password):
        return -3

    save_new_user(user_name, mail_address, password)

    return 0


def login(user_name, password):
    return password == get_password_from_user_name(user_name)



