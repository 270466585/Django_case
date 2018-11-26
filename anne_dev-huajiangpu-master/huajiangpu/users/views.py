from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .functions import *
from .models import *


def index(request):
    return render(request, 'users/user_order.html', locals())


def register(request):
    return render(request, 'users/user_register.html', locals())


def login(request):
    return render(request, 'users/user_login.html', locals())


def address(request):
    return render(request, 'users/user_address.html', locals())


# 注册逻辑
def register_handle(request):

    if check_request_params(request):
        # 数据入库
        User.objects.user_register(request)
        return redirect(reverse('users:index'))
    else:
        return redirect(reverse('users:login'))




