from utils.wrapper import *


def check_request_params(request):
    username = post(request, 'user_name')
    userpass = post(request, 'user_pass')

    if not 5 <= len(username) <= 20:
        return False

    if not 8 <= len(userpass) <= 20:
        return False

    return True
