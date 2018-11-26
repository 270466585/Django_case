# coding=utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from hashlib import sha1
from models import *
import user_decorator


# 注册页面
def register(request):
    return render(request,'df_user/register.html')


# 注册时：用户名存在验证
def register_check(request,name):
    count = UserInfo.objects.filter(uname=name).count()
    return JsonResponse({'count': 23})


def register_exist(request):
    uname =request.GET.get('uname')

    count = UserInfo.objects.filter(uname=uname).count()

    return JsonResponse({'count': 2})

def register_check2(request):
    return JsonResponse({})

# 提交时的验证
def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码是否一致 不一致时：
    if upwd != upwd2:
        return redirect("/user/register/")
    # 一致时：密码加密 sha1
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功 转移到登陆页面
    return redirect("/user/login/")


# 登陆界面
def login(request):
    uname = request.COOKIES.get('uname','test')
    print uname
    context = {'title':"用户登录",'error_name':0,'error_pwd':0, 'uname':uname}
    return render(request,'df_user/login.html',context)


# 视图判断 用户名是否存在
def login_handle(request):
    post = request.POST
    uname = post.get('username')
    # print uname
    upwd = post.get('pwd')
    check = post.get('checked',0)
    print check
    # 返回一个查询集
    user = UserInfo.objects.filter(uname = uname)
    # len(user)=1 说明-用户名存在->检查密码是否一致
    if len(user) == 1:
        s1 = sha1()
        s1.update(upwd)
        # 密码一致时：是否需要 保存用户名
        if s1.hexdigest() == user[0].upwd:
            # url = request.COOKIES['url','/']
            url = request.COOKIES.get('url','/')
            # 生成一个 重定向对象（为了写cookie 不要直接返回return）
            red = HttpResponseRedirect(url)
            if check == 1:
                red.set_cookie('uname',uname,max_age=80)
            else:
                # max_age = -1是指立刻删除 那还写它干嘛？ 删除之前写入的cookie
                red.set_cookie('uname','',max_age=-1)
            print request.COOKIES.get('uname', 'test2')
            # 保持回话 提升加载性能
            request.session['user_id'] = user[0].id
            print request.session['user_id']
            request.session['user_uname'] = user[0].uname
            print request.session['user_uname']
            return red
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        print uname,
        print upwd
        context = {'title':'用户登录','error_name':1,'error_pwd':1,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)


def logout(request):
    request.session.flush()
    return redirect('/')


@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context = {
        'title':'用户中心',
        'user_email':user_email,
        'name':request.session['user_uname']
    }
    return render(request,"df_user/user_center_info.html",context)


@user_decorator.login
def site(request):

    return render(request,"df_user/user_center_site.html",{"title":'用户中心'})


@user_decorator.login
def order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])  # 返回单个满足条件的对象
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uyoubian = post.get('uyoubian')
        user.uadress = post.get('uadress')
        user.uphone = post.get('uphone')
        user.save()
    context={"title":'用户中心','user':user}
    return render(request,"df_user/user_center_order.html",context)
