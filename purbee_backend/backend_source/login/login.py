from purbee_backend.backend_source.database.database_utilities import (
    save_new_user,
    check_password_for_user_name,
    get_user_by_name
)
import sys

from ..login.login_utilities import (
    password_secure
)


def sign_up(user_name, mail_address, password):

    print(password, file = sys.stderr)
    if password_secure(password):
        return save_new_user(user_name, mail_address, password)
    else:
        return 3


def sign_in(user_name, password):
    return check_password_for_user_name(user_name, password)



