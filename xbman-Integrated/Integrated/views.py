#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Create your views here.
import django
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
import json
import models
import user_models
from django.core import serializers
from django.contrib.auth.hashers import make_password
from plugins.Decorators import admin_Auth,system_Auth


def login(request):
    if request.method == "POST":

        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.valid_end_time: #设置了end time
                if django.utils.timezone.now() > user.valid_begin_time and django.utils.timezone.now()  < user.valid_end_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    #print 'session expires at :',request.session.get_expiry_date()
                    return HttpResponseRedirect('/index/')
                else:
                    return render(request,'login.html',{'login_err': 'User account is expired,please contact your IT guy for this!'})
            elif django.utils.timezone.now() > user.valid_begin_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    return HttpResponseRedirect('/index/')

        else:
            return render(request,'login.html',{'login_err': '您输入的用户名或密码错误,请重新输入！'})
    else:
        return render(request, 'login.html')

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

@login_required
def checkpasswork(request):
    if request.method=='POST':
        try:
            oidpassword=request.POST.get('oldpassword')
            password=request.POST.get('password')
            user= auth.authenticate(username=str(request.user),password=oidpassword)
            user.set_password(password)
            user.save()
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/index/")
            return HttpResponseRedirect("/login/")
        except AttributeError,e:
            return HttpResponseRedirect("/login/")

@login_required
@system_Auth
def index(request,authoritys):
    return render(request, 'index.html',{"Authority": authoritys,},
                  context_instance=RequestContext(request))

@login_required
@admin_Auth
def users(request):
    if request.method == "POST":
        try:
            if request.POST.get('admin'):
                user = user_models.UserProfile.objects.create_user(email=request.POST.get('email'),name=request.POST.get('username'),password=request.POST.get('password'),admin=True)
            else:
                user = user_models.UserProfile.objects.create_user(email=request.POST.get('email'),name=request.POST.get('username'),password=request.POST.get('password'))
            user.save()
            return HttpResponseRedirect("/users/")
        except Exception,e:
            return HttpResponseRedirect("/users/")
    else:
        contact_list = user_models.UserProfile.objects.all()
        paginator = Paginator(contact_list, 20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        # return contacts, group_list
        return render(request, 'users.html',{"topics": contacts},
                      context_instance=RequestContext(request))

@login_required
@admin_Auth
def del_user(request):
    if request.method == "POST":
        user_models.UserProfile.objects.get(email=request.POST.get('modify')).delete()
        return HttpResponse(json.dumps('true'))

@login_required
@admin_Auth
def gemail(request):
    if request.method == "GET":
        userget = user_models.UserProfile.objects.filter(email=request.GET.get('modify'))
        srvs_json = serializers.serialize("json", userget)
        return HttpResponse(srvs_json[1:-1])
    elif request.method == "POST":
        user = user_models.UserProfile.objects.get(email=request.POST.get('e_email'))
        user.name = request.POST.get('e_name')
        user.department = request.POST.get('e_department')
        user.mobile = request.POST.get('e_mobile')
        if request.POST.get('e_password').strip() != '':
            user.set_password=request.POST.get('e_password')
        if request.POST.get('e_admin') == None:
            user.is_admin = ''
        else:
            user.is_admin = 'True'
        if len(request.POST.get('e_password')) != 0:
            user.password=make_password(request.POST.get('e_password'))
        user.save()
        if str(request.user) == request.POST.get('e_email') and len(request.POST.get('e_password')) != 0:
            user = auth.authenticate(username=str(request.user), password=request.POST.get('e_password'))
            auth.login(request, user)
        return HttpResponseRedirect("/users/")

@login_required
@admin_Auth
def authority(request):
    if request.method == "GET":
        user_list = user_models.UserProfile.objects.all().values('name')
        contact_list = models.Authoritys.objects.all()
        paginator = Paginator(contact_list, 20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'authority.html',{"topics": contacts,"user_list":user_list},
                      context_instance=RequestContext(request))
    elif request.method == "POST":
        try:
            user = user_models.UserProfile.objects.get(name=request.POST.get('username'))
            models.Authoritys.objects.get_or_create(user_name=user,mark=1,Auth_name=request.POST.get('system'))
            return HttpResponseRedirect("/authority/")
        except Exception, e:
            return HttpResponseRedirect("/authority/")

@login_required
@admin_Auth
def delauth(request):
    if request.method == "POST":
        models.Authoritys.objects.get(id=request.POST.get('modify')).delete()
        return HttpResponse(json.dumps('true'))
