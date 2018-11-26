#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from froms import LoginForm
import time,json
import models
from plugins import modify_keepalived,build_jenkins,paramiko_cmd,svn_marge,modify_keepalived_Intranet
from Integrated.plugins.Decorators import admin_Auth,Perm_verification
# from vars import method_operation #并发svn模块


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

@login_required
@Perm_verification(perm='jenkins')
def index(request):
    routine = []
    notroutine = []
    for i in range(1,13):
        routine.append(models.Release.objects.filter(date__year=time.strftime("%Y", time.localtime())).filter(date__month=i).filter(type_list='routine').count())
        notroutine.append(models.Release.objects.filter(date__year=time.strftime("%Y", time.localtime())).filter(date__month=i).filter(type_list='notroutine').count())
    return render_to_response('releases/index.html',{'routine':routine,'notroutine':notroutine,'date':time.strftime("%Y", time.localtime())}, context_instance=RequestContext(request))



@login_required
@Perm_verification(perm='jenkins')
def tables(request):
    contact_list = models.Release.objects.all().order_by('-id' )
    paginator = Paginator(contact_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('releases/tables.html', {"topics": contacts},context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jenkins')
def lvsmodify(request):
    if request.method == 'POST':
        models.lvsmodify.objects.all().delete()
        models.lvsmodify.objects.create(username=request.POST.get('username'),
                                        password=request.POST.get('password'),
                                        IP=request.POST.get('ipdizhi'),
                                        IntranetIP=request.POST.get('ipdizhi2'),
                                        ScriptLocation=request.POST.get('jiaoben'),
                                        onegroup=request.POST.get('onegroup'),
                                        twogroup=request.POST.get('twogroup'),
                                        Intranetonegroup=request.POST.get('Intranetonegroup'),
                                        Intranettwogroup=request.POST.get('Intranettwogroup'),
                                        Remark=request.POST.get('Remark')).save()
        modify = models.lvsmodify.objects.all()
        return render_to_response('releases/lvsmodify.html', {'modify': modify[0],'zhuangtai':True},
                                  context_instance=RequestContext(request))
    else:
        modify = models.lvsmodify.objects.all()
        if  len(modify) == 0:
            return render_to_response('releases/lvsmodify.html',{'modify':modify},context_instance=RequestContext(request))
        else:
            return render_to_response('releases/lvsmodify.html', {'modify': modify[0]},context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jenkins')
def jenkinsmodify(request):
    if request.method == 'POST':
        models.jenkinsmodify.objects.all().delete()
        models.jenkinsmodify.objects.create(username=request.POST.get('username'), password=request.POST.get('password'),
                                        UrlLocation=request.POST.get('urllocation'),Remark=request.POST.get('Remark')).save()
        modify = models.jenkinsmodify.objects.all()
        return render_to_response('releases/jenkinsmodify.html', {'modify': modify[0],'zhuangtai':True},
                                  context_instance=RequestContext(request))
    else:
        modify = models.jenkinsmodify.objects.all()
        if len(modify) == 0:
            return render_to_response('releases/jenkinsmodify.html', {'modify': modify}, context_instance=RequestContext(request))
        else:
            return render_to_response('releases/jenkinsmodify.html', {'modify': modify[0]},context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jenkins')
def publishmodify(request):
    views_list = []
    obj = models.jenkinsmodify.objects.all()
    try:
        date = build_jenkins.buildjob(obj).get_jeknins()
        for item in date:
            views_list.append(item['name'])
    except BaseException,e:
        views_list.append('系统暂时不能连接至jenkins，请检查jenkins配置是否正确！')
    if request.method == 'POST':
        models.publishmodify.objects.all().delete()
        models.publishmodify.objects.create(onegroup=request.POST.get('onegroup'),
                                            twogroup=request.POST.get('twogroup'),
                                            Remark=request.POST.get('Remark')).save()
        modify = models.publishmodify.objects.all()
        return render_to_response('releases/publishmodify.html', {'modify': modify[0],'zhuangtai':True,'views_list':views_list},
                                  context_instance=RequestContext(request))
    else:
        modify = models.publishmodify.objects.all()
        if len(modify) == 0:
            return render_to_response('releases/publishmodify.html', {'modify': modify,'views_list':views_list},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('releases/publishmodify.html', {'modify': modify[0],'views_list':views_list},
                                      context_instance=RequestContext(request))


@login_required
@Perm_verification(perm='jenkins')
def hostshmodify(request):
    if request.method == 'POST':
        models.hostshmodify.objects.all().delete()
        models.hostshmodify.objects.create(IP=request.POST.get('saltip'),
                                           username=request.POST.get('saltusername'),
                                           password=request.POST.get('saltpasswork'),
                                           onegroup=request.POST.get('onegroup'),
                                           twogroup=request.POST.get('twogroup'),
                                           reductionone=request.POST.get('reductionone'),
                                           reductiontwo=request.POST.get('reductiontwo'),
                                           Remark=request.POST.get('Remark')).save()
        modify = models.hostshmodify.objects.all()
        return render_to_response('releases/hostsmodify.html', {'modify': modify[0], 'zhuangtai': True},
                              context_instance=RequestContext(request))
    else:
        modify = models.hostshmodify.objects.all()
        if len(modify) == 0:
            return render_to_response('releases/hostsmodify.html', {'modify': modify}, context_instance=RequestContext(request))
        else:
            return render_to_response('releases/hostsmodify.html', {'modify': modify[0]}, context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jenkins')
def relemanager(request):
    return render_to_response('releases/relemanager.html',{'modify':'未获取'},context_instance=RequestContext(request))

def ipvsadm(request):
    if request.method == 'POST':
        obj = models.lvsmodify.objects.all()
        IPVS = modify_keepalived.modify_keep(obj, '0', '0', 'down').ipvsadm()
        IPVS1 = modify_keepalived_Intranet.modify_keep(obj, '0', '0', 'down').ipvsadm()
        data = {'status': 0, 'msg': '请求成功', 'data': '外:'+IPVS+'内:'+IPVS1}
        return HttpResponse(json.dumps(data))

def odline(request):
    if request.method == 'POST':
        obj = models.lvsmodify.objects.all()
        if request.POST['modify'] == '1':
            date = modify_keepalived.modify_keep(obj,'1','0','down').Landed()
            RE = modify_keepalived.modify_keep(obj,'1','0','down').Reload()
            IPVS = modify_keepalived.modify_keep(obj,'1','0','down').ipvsadm()
            date2 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'down').Landed()
            RE2 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'down').Reload()
            IPVS2 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'down').ipvsadm()
            data = {'status':0,'msg':'请求成功','data':date+RE+date2+RE2,'ipvsadm':'外:'+IPVS+'内:'+IPVS2}
            return HttpResponse(json.dumps(data))
        elif request.POST['modify'] == '2':
            date1 = modify_keepalived.modify_keep(obj, '1','0', 'up').Landed()
            date2 = modify_keepalived.modify_keep(obj, '2','0', 'down').Landed()
            RE = modify_keepalived.modify_keep(obj, '1','0', 'down').Reload()
            IPVS = modify_keepalived.modify_keep(obj,'1','0','down').ipvsadm()
            date3 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'up').Landed()
            date4 = modify_keepalived_Intranet.modify_keep(obj, '2', '0', 'down').Landed()
            RE1 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'down').Reload()
            IPVS1 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'down').ipvsadm()
            data = {'status':0,'msg':'请求成功','data':date1+date2+RE+date3+date4+RE1,'ipvsadm':'外:'+IPVS+'内:'+IPVS1}
            return HttpResponse(json.dumps(data))
        elif request.POST['modify'] == '3':
            date2 = modify_keepalived.modify_keep(obj, '2','0', 'up').Landed()
            RE = modify_keepalived.modify_keep(obj, '1','0', 'down').Reload()
            IPVS = modify_keepalived.modify_keep(obj, '1','0', 'down').ipvsadm()
            date3 = modify_keepalived_Intranet.modify_keep(obj, '2', '0', 'up').Landed()
            RE1 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'down').Reload()
            IPVS1 = modify_keepalived_Intranet.modify_keep(obj, '1', '0', 'down').ipvsadm()
            data = {'status': 0, 'msg': '请求成功', 'data':date2+RE+date3+RE1,'ipvsadm':'外:'+IPVS+'内:'+IPVS1}
            return HttpResponse(json.dumps(data))
        elif request.POST['modify'] == '4':
            if request.POST['date'].split(' ')[1] == 'down':
                date1 = modify_keepalived.modify_keep(obj,'3',request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).Landed()
                # 执行reload
                RE = modify_keepalived.modify_keep(obj, '3',request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).Reload()
                IPVS = modify_keepalived.modify_keep(obj, '1',request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).ipvsadm()
                data = {'status': 0, 'msg': '请求成功', 'data': date1+ RE + 'ipvsadm数:%s'%IPVS}
                return HttpResponse(json.dumps(data))
            elif request.POST['date'].split(' ')[1] == 'up':
                try:
                    if request.POST['date'].split(' ')[3] == 'down':
                        date1 = modify_keepalived.modify_keep(obj, '3',request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).Landed()
                        date2 = modify_keepalived.modify_keep(obj, '3',request.POST['date'].split(' ')[2],request.POST['date'].split(' ')[3]).Landed()
                        RE = modify_keepalived.modify_keep(obj, '3',request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).Reload()
                        IPVS = modify_keepalived.modify_keep(obj, '3',request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).ipvsadm()
                        data = {'status': 0, 'msg': '请求成功', 'data': date1 + date2 + RE + 'ipvsadm数:%s'%IPVS}
                        return HttpResponse(json.dumps(data))
                except IndexError, e:
                    date2 = modify_keepalived.modify_keep(obj, '3', request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).Landed()
                    RE = modify_keepalived.modify_keep(obj, '3', request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).Reload()
                    IPVS = modify_keepalived.modify_keep(obj, '3', request.POST['date'].split(' ')[0],request.POST['date'].split(' ')[1]).ipvsadm()
                    data = {'status': 0, 'msg': '请求成功', 'data':date2 + RE + 'ipvsadm数:%s' % IPVS}
                    return HttpResponse(json.dumps(data))

def onrelease(request):
    if request.method == 'POST':
        obj = models.jenkinsmodify.objects.all()
        obj2 = models.publishmodify.objects.all()
        if request.POST['modify'] == '1':
            date = build_jenkins.buildjob(obj).checkjob(obj2[0].onegroup.split(','))
            if date != None:
                data = {'status': 1, 'msg': 'Jenkins项目检测失败', 'data':date}
                return HttpResponse(json.dumps(data))
            else:
                date = build_jenkins.buildjob(obj).buildjobs(obj2[0].onegroup.split(','))
                data = {'status': 0, 'msg': '请求成功', 'data':date}
                return HttpResponse(json.dumps(data))
        elif request.POST['modify'] == '2':
            date = build_jenkins.buildjob(obj).checkjob(obj2[0].twogroup.split(','))
            if date != None:
                data = {'status': 1, 'msg': 'Jenkins项目检测失败', 'data': date}
                return HttpResponse(json.dumps(data))
            else:
                date = build_jenkins.buildjob(obj).buildjobs(obj2[0].twogroup.split(','))
                models.Release.objects.create(release=obj2[0].twogroup.split(','),type_list='routine').save()
                data = {'status': 0, 'msg': '请求成功', 'data': date}
                return HttpResponse(json.dumps(data))
        elif request.POST['modify'] == '3':
            print request.POST['date'].split(',')
            date = build_jenkins.buildjob(obj).checkjob(request.POST['date'].split(','))
            if date != None:
                data = {'status': 1, 'msg': 'Jenkins项目检测失败', 'data': date}
                return HttpResponse(json.dumps(data))
            else:
                date = build_jenkins.buildjob(obj).buildjobs(request.POST['date'].split(','))
                models.Release.objects.create(release=request.POST['date'].split(','), type_list='notroutine').save()
                data = {'status': 0, 'msg': '请求成功', 'data': date}
                return HttpResponse(json.dumps(data))


def hostsoperate(request):
    if request.method == 'POST':
        obj = models.hostshmodify.objects.all()
        if request.POST['modify'] == '1':
            date = paramiko_cmd.modify_paramiko(obj[0].IP,obj[0].username,obj[0].password).Landed(obj[0].onegroup)
            data = {'status': 0, 'msg': '请求成功', 'data':date}
            return HttpResponse(json.dumps(data))
        elif request.POST['modify'] == '2':
            date = paramiko_cmd.modify_paramiko(obj[0].IP, obj[0].username, obj[0].password).Landed(obj[0].twogroup)
            data = {'status': 0, 'msg': '请求成功', 'data': date}
            return HttpResponse(json.dumps(data))

def hostsreduction(request):
    if request.method == 'POST':
        obj = models.hostshmodify.objects.all()
        if request.POST['modify'] == '1':
            date = paramiko_cmd.modify_paramiko(obj[0].IP, obj[0].username, obj[0].password).Landed(obj[0].reductionone)
            data = {'status': 0, 'msg': '请求成功', 'data': date}
            return HttpResponse(json.dumps(data))
        elif request.POST['modify'] == '2':
            date = paramiko_cmd.modify_paramiko(obj[0].IP, obj[0].username, obj[0].password).Landed(obj[0].reductiontwo)
            data = {'status': 0, 'msg': '请求成功', 'data': date}
            return HttpResponse(json.dumps(data))

@login_required
@Perm_verification(perm='jenkins')
def onlyrelease(request):
    return render_to_response('releases/onlyrelease.html', context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jenkins')
def onlylvs(request):
    return render_to_response('releases/onlylvs.html', context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jenkins')
def svnmarge(request):
    return render_to_response('releases/svnmarge.html',context_instance=RequestContext(request))


def magre(request):
    if request.method == 'POST':
        logs = []
        svn_date = request.POST['date']
        # date = method_operation.Svninfo().start(svn_date) #并发
        for item in svn_date:
            log = svn_marge.marge_svn(item).run()
            for i in log:
                logs.append(i)
        data = {'status': 0, 'msg': '请求成功', 'data': ''.join(logs)}
        return HttpResponse(json.dumps(data))