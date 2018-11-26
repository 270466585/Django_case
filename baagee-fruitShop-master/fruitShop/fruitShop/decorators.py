# coding=utf-8
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def check_user_login(func):
    def check_login(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            redirect = HttpResponseRedirect(reverse('fruitShop:user_login'))
            # 保存要跳转的链接
            redirect.set_cookie('to_url', request.get_full_path())
            return redirect

    return check_login
