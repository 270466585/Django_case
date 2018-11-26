# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render, redirect, render_to_response
from models import Post,User
from markdown2 import markdown
from forms import EditForm,RegisterForm,LoginForm,EditForm

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.template.context import RequestContext
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger


logger = logging.getLogger('blog.views')

# Create your views here.
def index(request):

    return render(request,'index.html',locals())



def article(request):
    posts  = Post.objects.filter(status= '2' )
    paginator = Paginator(posts, 12)
    try:
        page = int(request.GET.get('page', 1))
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        posts = paginator.page(1)

    # for page in posts.paginator.page_range:

    return render(request, 'article.html', {'posts':posts})

def about(request):

    return render(request,'about.html',locals())


def post(request,p_id):
    obj = Post.objects.get(id = int(p_id))
    obj.click_count = obj.click_count + 1
    obj.save()
    obj.body = markdown(obj.body)
    data = {
        'obj': obj
    }

    return render(request, 'detail.html', data)

@login_required(login_url='/login/')
def xuser(request):
    user_id = request.user.id
    obj = Post.objects.filter(user = int(user_id))

    # print(obj)

    data = {
        'obj': obj
    }

    return render(request,'xuser.html',data)


@login_required(login_url='/login/')
def editarticle(request, p_id):
    obj = Post.objects.get(id = int(p_id))
    # form = EditForm(request.POST or None,instance = obj)
    if obj.status == '0':
        status = '待审核'
    elif obj.status == '1':
        status = '待发布'
    elif obj.status == '2':
        status = '已发布'
    elif obj.status == '3':
        status = '抱歉，未通过审核'

    form = EditForm(initial={'id': obj.id, 'title':obj.title,'desc':obj.desc,
                             'img_link':obj.img_link,'music_link':obj.music_link,'body':obj.body,
                             'status': status, 'user': obj.user})

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['status'] == u'待审核':
                status = '0'

                post = Post()
                post.id = form.cleaned_data['id']
                post.title = form.cleaned_data['title']
                post.desc = form.cleaned_data['desc']
                post.img_link = form.cleaned_data['img_link']
                post.music_link = form.cleaned_data['music_link']
                post.body = form.cleaned_data['body']
                post.status = status
                post.date_publish = obj.date_publish
                post.user = obj.user

                post.save()
                messages.add_message(request, messages.SUCCESS, '保存文章成功！请耐心等待编辑审核！')
                return redirect('/xuser/')
            else:
                pass
        else:
            messages.add_message(request, messages.ERROR, '保存文章失败！请检查各项输入是否完全！')
    else:
        form = EditForm(initial={'id': obj.id, 'title': obj.title, 'desc': obj.desc,
                                 'img_link': obj.img_link, 'music_link': obj.music_link, 'body': obj.body,
                                 'status': status, 'user': obj.user})
    data ={
        'obj':obj,
        'form':form,
    }
    return render(request,'editarticle.html',data)


@login_required(login_url='/login/')
def addarticle(request):
    post = Post.objects.order_by('-id')[0:1]
    for post in post:
        id  = post.id +1
    user =  request.user

    if request.method == 'POST':
        form = EditForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['status'] == u'待审核':
                status = '0'

                post = Post()
                post.id = form.cleaned_data['id']
                post.title = form.cleaned_data['title']
                post.desc = form.cleaned_data['desc']
                post.img_link = form.cleaned_data['img_link']
                post.music_link = form.cleaned_data['music_link']
                post.body = form.cleaned_data['body']
                post.status = status
                post.user = user

                post.save()
                # print('ok')
                messages.add_message(request, messages.SUCCESS, '保存文章成功！请耐心等待编辑审核！')
                return redirect('/xuser/')
            else:
                pass
        else:
            messages.add_message(request, messages.ERROR, '保存文章失败！请检查各项输入是否完全！')
    else:
        form = EditForm(initial={'id': id, 'status': '待审核', 'user': user})
        data = {
            'form': form
        }

    return render(request, 'addarticle.html', data)
# @login_required(login_url='/login/')
# def addarticle(request):
#     #设置默认的id,status,user
#     post = Post.objects.order_by('-id')[0:1]
#     for post in post:
#         id  = post.id +1
#     user =  request.user.id
#     status = 0
#     obj = Post()
#     obj.id = id
#     obj.user_id = user
#     obj.status = status
#
#     #将默认的信息写入表单
#     form = EditForm(request.POST or None, instance=obj)
#
#
#
#     id  = request.POST.get('id')
#     title = request.POST.get('title')
#     desc = request.POST.get('desc')
#     img_link = request.POST.get('img_link')
#     music_link = request.POST.get('music_link')
#     body = request.POST.get('body')
#     user_id = request.POST.get('user_id')
#     status = request.POST.get('status')
#
#     # newpost = Post()
#     # newpost.id = id
#     # newpost.title = title
#     # newpost.desc = desc
#     # newpost.img_link = img_link
#     # newpost.music_link = music_link
#     # newpost.body =body
#     # newpost.user_id = user_id
#     # newpost.status = status
#
#     print(id)
#     print(title)
#     print(desc)
#     print(img_link)
#     print(music_link)
#     print(body)
#     print(user_id)
#     print(status)
#     #
#     print(form)
#     if form.is_valid():
#         form.save()
#         messages.add_message(request, messages.SUCCESS, '添加文章成功！请耐心等待编辑审核！')
#     #
#     # form = EditForm()
#     # print(form)
#     # if form.is_valid():
#     #     form.save()
#     # print(form)
#     return render(request,'addarticle.html',{'form':form})


@login_required(login_url='/login/')
def PersonalCenter(request):
    pass

    return render(request,'PersonalCenter.html',{})


def do_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            pass_word = form.cleaned_data['password']
            print(user_name)
            print(pass_word)
            user = authenticate(username=user_name, password=pass_word)
            print(user)
            if user is not None:
                print(user)
                login(request, user)
                messages.add_message(request, messages.SUCCESS, '登录成功！')
                return render(request, 'login.html', {'form':form})
            else:
                messages.add_message(request, messages.ERROR, '登录失败')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})

    # return render(request, 'login.html', locals())


def do_register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if (form.cleaned_data['password'] == form.cleaned_data['password2']) is False:
                messages.add_message(request,messages.ERROR,'两次输入的密码不一致！')

            elif len(User.objects.filter(username=form.cleaned_data['username'])) > 0:
                messages.add_message(request, messages.ERROR, '该用户名已经被注册了，请换一个名字注册！')

            elif len(User.objects.filter(email=form.cleaned_data['email'])) > 0:
                messages.add_message(request, messages.ERROR, '该邮箱已经被注册了，请换一个邮箱注册！')

            else:
                # user = User.objects.create(username=form.cleaned_data['username'],
                #                                 email=form.cleaned_data['email'],
                #                                 password= make_password(form.cleaned_data['password']))
                user = User()
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.password= make_password(form.cleaned_data['password'])

                user.save()
                messages.add_message(request, messages.SUCCESS, '恭喜，注册成功！')
        else:
            return render(request, 'register.html', {'reason': form.errors})

    else:
        form = RegisterForm()

    return render(request, 'register.html', locals())


def do_logout(request):
    logout(request)

    return render(request,'index.html')