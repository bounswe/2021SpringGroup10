import re


def password_secure(password):
    reg = "^(?=.*[A-Z])(?=.*[!@#$&*.,*%+-/])(?=.*[0-9])(?=.*[a-z]).{8,}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat:
        return True
    else:
        return False
