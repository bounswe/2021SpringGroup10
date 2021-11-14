from purbee_backend.backend_source.database.database_utilities import (
    save_new_user,
    check_password_for_user_name,
    get_user_by_name,
    update_profile_info_by_user_name,
    check_user_by_user_name,
    get_profile_page_by_user_name
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

def update_profile_page(user_name,profile_photo,bio,first_name,last_name,birth_date):
    if check_user_by_user_name(user_name):
        #no such user
        return 1
    else:
        code = update_profile_info_by_user_name(user_name,profile_photo,bio,first_name,last_name,birth_date)
        if code:
            #database error
            return 2
        else:
            return 0

def get_profile_page(user_name):
    if check_user_by_user_name(user_name):
        # no such user
        return 1
    else:
        result = get_profile_page_by_user_name(user_name)
        if not result:
            #database error
            return 2
        else:
            return result



