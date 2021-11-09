from purbee_backend.backend_source.database.database_utilities import (
    save_new_user,
    check_password_for_user_name
)

from login_utilities import (
    password_secure
)


def sign_up(user_name, mail_address, password):

    try:
        assert password_secure(password)
    except AssertionError:
        return 3

    return save_new_user(user_name, mail_address, password)


def sign_in(user_name, password):
    return check_password_for_user_name(user_name, password)



