# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid

from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from app1 import models

# Create your views here.
def taskList(request):
    data=[]
    project_list = models.project_model.objects.all()
    index = 1
    for i in project_list:
        projectGuid = i.projectGuid
        plan_list = models.plan_model.objects.filter(projectGuid=projectGuid)
        for j in plan_list:
            planGuid = j.planGuid
            turn_list = models.turn_model.objects.filter(planGuid=planGuid)
            for k in turn_list:
                tmp_list = []
                tmp_list.append(index)
                tmp_list.append(j.type)
                tmp_list.append(i.projectName)
                tmp_list.append(j.planName)
                tmp_list.append(k.turnName)
                tmp_list.append(k.content)
                tmp_list.append(k.tester)
                tmp_list.append(k.startTime)
                tmp_list.append(k.endTime)
                tmp_list.append(k.workHour)
                tmp_list.append(k.mark)
                tmp_list.append(k.turnGuid)
                data.append(tmp_list)
                index = index + 1
    return render(request, 'taskList.html',{'data':data})

def addProject(request):
    if request.method == 'POST':  # 当提交表单时
        projectName = request.POST['projectName']
        list = models.project_model.objects.filter(projectName=projectName)
        if(list.count() > 1):
            msg = '已经存在此项目'
            return render(request,'addProject.html', {'msg':msg})
        projectUrl = request.POST['projectUrl']
        projectGuid = uuid.uuid4()
        obj = models.project_model(projectName=projectName,projectUrl=projectUrl,projectGuid=projectGuid)
        obj.save()
        return HttpResponseRedirect('/taskList/')
    else:  # 当正常访问时
        return render(request, 'addProject.html')

def deleteTurn(request):
    pass

def addPlan(request):
    if request.method == 'POST':  # 当提交表单时
        projectName = request.POST['projectName']
        projectGuid = models.project_model.objects.get(projectName=projectName).projectGuid
        planName = request.POST['planName']
        planGuid = uuid.uuid4()
        isMail = '无'
        isReport = '无'
        isBeautiful = '无'
        type = request.POST['type']
        isApp = request.POST['isApp']
        obj = models.plan_model(planName=planName,planGuid=planGuid,projectGuid=projectGuid,isMail=isMail,isReport=isReport,isBeautiful=isBeautiful,type=type,isApp=isApp)
        obj.save()
        return HttpResponseRedirect('/taskList/')
    else:  # 当正常访问时
        project_list = models.project_model.objects.all()
        return render(request, 'addPlan.html',{'data':project_list})

def addTurn(request):
    if request.method == 'POST':  # 当提交表单时
        planName = request.POST['planName']
        projectName = request.POST['projectName']
        projectGuid = models.project_model.objects.get(projectName=projectName).projectGuid
        planGuid = models.plan_model.objects.filter(projectGuid=projectGuid,planName=planName)[0].planGuid
        turnName = request.POST['turnName']
        turnGuid = uuid.uuid4()
        content = request.POST['content']
        # tester = request.POST['tester']
        tester_list = request.POST.getlist('tester[]')
        tester = ''
        for i in tester_list:
            tester = tester + i + ';'
        startTime = request.POST['startTime']
        endTime = request.POST['endTime']
        workHour = request.POST['workHour']
        mark = request.POST['mark']
        obj = models.turn_model(planGuid=planGuid,turnName=turnName,turnGuid=turnGuid,content=content,tester=tester,startTime=startTime,endTime=endTime,workHour=workHour,mark=mark)
        obj.save()
        return HttpResponseRedirect('/taskList/')
    else:  # 当正常访问时
        project_list = models.project_model.objects.all()
        data = []
        for i in project_list:
            projectName = i.projectName
            data.append(projectName)
        return render(request, 'addTurn.html',{'data':data})

def getPlanName(request,projectName):
    if request.method == 'GET':
        data = []
        projectGuid = models.project_model.objects.filter(projectName=projectName)[0].projectGuid
        plan_list = models.plan_model.objects.filter(projectGuid=projectGuid)
        for i in plan_list:
            data.append(i.planName)
        return HttpResponse(json.dumps(data), content_type='application/json')


def delete(request,guid):
    models.turn_model.objects.filter(turnGuid=guid).delete()
    return HttpResponseRedirect('/taskList/')

def projectList(request):
    if request.method == 'GET':
        project_list = models.project_model.objects.all()
        data = []
        index = 1
        for i in project_list:
            list = []
            projectName = i.projectName
            projectGuid = i.projectGuid
            list.append(index)
            list.append(projectName)
            list.append(projectGuid)
            data.append(list)
            index = index + 1
        return render(request, 'projectList.html', {'data': data})

def projectDetail(request,projectGuid):
    plan_list = models.plan_model.objects.filter(projectGuid=projectGuid)
    data = {}
    for i in plan_list:
        planGuid = i.planGuid
        planName = i.planName
        turn_list = models.turn_model.objects.filter(planGuid=planGuid)
        index = 1
        listall = []
        for j in turn_list:
            list = []
            list.append(index)
            list.append(j.turnName)
            list.append(j.content)
            list.append(j.tester)
            list.append(j.startTime)
            list.append(j.endTime)
            list.append(j.mark)
            listall.append(list)
            index = index + 1
        data[planName] = listall
    return render(request, 'projectDetail.html',{'data':data})

def statistics(request):
    if request.method == 'GET':
        year_month = ['2016.12','2017.01','2017.02','2017.03','2017.04','2017.05','2017.06','2017.07','2017.08','2017.09','2017.10','2017.11','2017.12']
        # year_month.sort()
        data = {}

        data1 = {}
        for i in year_month:
            year = i.split('.')[0]
            month = i.split('.')[1]
            turn_list = models.turn_model.objects.filter(startTime__year=year,startTime__month=month)
            list = []
            for j in turn_list:
                list.append(j.planGuid)
            new_list = []
            for k in list:
                if k not in new_list:
                    new_list.append(k)
            data1[i] = [len(new_list),len(turn_list)]

        data11 = sorted(data1.items(), key=lambda d: d[0], reverse=False)

        data2 = []
        projectCount = len(models.project_model.objects.all())
        planCount = len(models.plan_model.objects.all())
        turnCount = len(models.turn_model.objects.all())
        data2 = ['2017',projectCount,planCount,turnCount]

        data3 = {}
        tester = ['顾疆飞','姜志伟','田园','杨剑','陈嘉祎','何雷雷','黄志佼','徐静']
        for i1 in tester:
            turn_list2 = models.turn_model.objects.filter(tester__contains=i1)
            list = []
            for j1 in turn_list2:
                list.append(j1.planGuid)
            new_list = []
            for k1 in list:
                if k1 not in new_list:
                    new_list.append(k1)
            data3[i1] = [len(new_list), len(turn_list2)]

        data['data1'] = data11
        data['data2'] = data2
        data['data3'] = data3

        return render(request, 'statistics.html',{'data':data})