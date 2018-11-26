import hashlib
from django.contrib import messages


# 方法log
def function_log(out_func):
    def wrapper(*args, **kwargs):
        print('function start ---------', str(out_func))
        temp = out_func(*args, **kwargs)
        print('function end ---------', str(out_func))
        return temp
    return wrapper


# POST
def post(request, key):
    return request.POST.get(key, '').strip()


# GET
def get(request, key):
    return request.GET.get(key, '').strip()


# 保存cookie
def set_cookie(response, key, value):
    response.set_cookie(key, value, max_age=60*60*24)


# 获取cookie
def get_cookie(request, key):
    return request.COOKIES.get(key, '')


# 删除cookie
def del_cookie(request, key):
    request.delete_cookie(key)


# 保存session
def set_session(request, key, value):
    request.session[key] = value


# 获取session
def get_session(request, key):
    return request.session.get(key, '')


# 删除session
def del_session(request):
    request.session.flush()


# 密码加密函数
def password_encryption(password, salt=''):
    new_pw = '*&**(*W' + password + 'UD*FDS(*&' + salt
    sha = hashlib.sha256()
    sha.update(new_pw.encode('utf-8'))
    return sha.hexdigest()


# 修改添加消息的方法
def set_message(request, key, value):
    messages.add_message(request, messages.INFO, key + ':' + value)


# 获取消息
def get_message(request):
    megs = messages.get_messages(request)
    dic_msg = {}
    for meg in megs:
        list_meg = str(meg).split(':')
        dic_msg[list_meg[0]] = list_meg[1]
    return dic_msg





