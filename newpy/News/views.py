from django.shortcuts import render_to_response,render
from News import models
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django_comments import models as comments_models
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from News.zh import main
from datetime import datetime

def sort(wl):
    wl=wl.split(':')
    l1=0
    l2=0
    for i in wl:
        if i is None:
            return {'l1': l1, 'l2': l2}
        else:
            if int(i)==1:
                l1+=1
            elif int(i)==2:
                l2+=1
    return {'l1':l1,'l2':l2}

def index(request):
    # models.New.objects.create(
    #     u='cb',
    #     key=0,
    #     start_time=0,
    #     end_time=0,
    # );
    time=models.New.objects.get(u='cb')
    if time.key==0:
        p = main()
        p.getpage()
        time.start_time=str(datetime.now()).split()[1].split(':')[0]
        time.key+=1

    time.end_time=str(datetime.now()).split()[1].split(':')[0]
    if (int(time.end_time)-int(time.start_time))>8:
        time.key=0
    time.save()
    # 从数据库中取出bbs数据渲染到index.html中
    #bbs_list=list()
    n=0
    # for i in l:
    #     bbs_list.append(i)
    #     n+=1
    #     if n >=20:
    #         break
    # 取出bbs的类别
    if str(request.user) == 'AnonymousUser':
        print('123453')
        bbs_list = models.BBS.objects.order_by('created_at')
    else:
        author=models.BBS_user.objects.get(user__username=request.user)
        wl=author.user_bbs_id
        result=sort(wl)
        if result['l2']>result['l1']:
            bbs_list=models.BBS.objects.order_by('bbs_category')
        else:
            bbs_list = models.BBS.objects.order_by('-bbs_category')
    bbs_categories = models.Category.objects.all()
    bbs_user=models.BBS_user.objects.all()
    bbs_id=0
    user=request.user
    return  render(request,'index.html',locals())

def search(request):
    content=request.POST.get('searh')

    bbs_list=models.BBS.objects.filter(title__contains=content)

    # bbs_list = models.BBS.objects.order_by('created_at')
    bbs_categories = models.Category.objects.all()
    bbs_user=models.BBS_user.objects.all()
    bbs_id=0
    user=request.user
    return  render(request,'index.html',locals())

# bbs分类
def category(request, cate_id):
    bbs_list = models.BBS.objects.filter(category__id=cate_id)
    bbs_categories = models.Category.objects.all()
    return render_to_response('index.html', {'bbs_list': bbs_list,
                                             'user': request.user,
                                             'bbs_category': bbs_categories,
                                             'bbs_id': int(cate_id),
                                             })


def bbs_detail(request,d):
    author=models.BBS_user.objects.get(user__username=request.user)
    bbs_obj=models.BBS.objects.get(id=d)
    bbs_obj.view_count+=1
    author.user_bbs_id+=":"+str(bbs_obj.bbs_category_id)
    bbs_obj.save()
    author.save()
    user=request.user
    return render(request,'bbs_detail.html',locals())

@csrf_exempt
def sub_comment(request,bbs_id):
    if request.is_ajax():
        coment=request.POST.get('content')
        if coment:
           # bbs_id = request.POST.get('bbs_id')
            bbs=models.BBS.objects.get(id=bbs_id)
            bbs.say_count += 1
            # comment = request.POST.get('comment_content')
            c = comments_models.Comment()
            c.comment = coment
            c.object_pk = bbs_id
            c.content_type_id = 13
            c.site_id = 1
            c.user = request.user
            comments_models.Comment.save(c)
            bbs.save()
            return HttpResponse(json.dumps({"content": coment}))


    # bbs_id=request.POST.get('bbs_id')
    # bbs=models.BBS.objects.get(id=bbs_id)
    # bbs.say_count+=1
    # comment=request.POST.get('comment_content')
    # c=comments_models.Comment()
    # c.comment=comment
    # c.object_pk=bbs_id
    # c.content_type_id=7
    # c.site_id=1
    # c.user=request.user
    # comments_models.Comment.save(c)
    # bbs.save()
    # return HttpResponseRedirect('/detail/%s' %bbs_id)

def acc_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        content='''
        Welcome %s !!!
        <a href='/logout/' >Logout</a>
        '''%user.username
        return HttpResponseRedirect('/')

def logout_view(request):
    user=request.user
    auth.logout(request)
    return HttpResponse("<b>%s</b> logge out! <br/><a href='/'>Re_login</a>" %user)

def Login(request):
    return render(request, 'zh.html')

def bbs_pub(request):

    return render(request,'sub_pub.html')

def bbs_sub(request):
    author=models.BBS_user.objects.get(user__username=request.user)
    picture_name=request.POST.get('summary_pictrue')
    # picture=request.FILES['summary_pictrue']
    # print(picture)
    # print(picture)
    # print(picture)
    class_id=request.POST.get('class')
    title = request.POST.get('title')
    content = request.POST.get('content')
    summary = request.POST.get('summary')
    models.BBS.objects.create(
        title=title,
    picture=picture_name,
    bbs_category_id=int(class_id),
    summary = summary,
    content = content,
    author = author,

    )
    return HttpResponse("<h2>恭喜您，文章发布成功, 按 <br/><a href='/'>返回</a> 主页面!<h2>")

def reg(request):
    return render(request,'zhreg.html')


def log(request):
    return render(request,'zh.html')

def acc_reg(request):
    name=request.POST.get('username')
    pawd=request.POST.get('password')
    u=models.User(username=name)
    u.set_password(pawd)
    u.save()
    obj=models.BBS_user()
    obj.user=u
    obj.user_bbs_id=1
    obj.save()
    # obj=models.BBS_user.user
    #
    # obj.Username=name
    # obj.Password=pawd
    # obj.save()
    # obj=models.BBS_user.objects.get(user__username=request.user)
    # models.BBS_user.objects.create(
    #     Username=request.GET('username'),
    #     Password=request.GET('password'),
    # )
    # obj.username=request.GET('username')
    # obj.password=request.GET('password')
    # obj.save()
    # return HttpResponseRedirect('/','注册成功！')
    return HttpResponse('注册成功！')

def technology(request):
    # models.New.objects.create(
    #     u='cb',
    #     key=0,
    #     start_time=0,
    #     end_time=0,
    # );
    # time = models.New.objects.get(u='cb')
    # if time.key == 0:
    #     p = main()
    #     p.getpage()
    #     time.start_time = str(datetime.now()).split()[1].split(':')[0]
    #     time.key += 1
    #
    # time.end_time = str(datetime.now()).split()[1].split(':')[0]
    # if (int(time.end_time) - int(time.start_time)) > 8:
    #     time.key = 0
    # time.save()
    # 从数据库中取出bbs数据渲染到index.html中
    # bbs_list=list()
    n = 0
    # for i in l:
    #     bbs_list.append(i)
    #     n+=1
    #     if n >=20:
    #         break

    # 取出bbs的类别
    author = models.BBS_user.objects.get(user__username=request.user)
    wl = author.user_bbs_id
    # result = sort(wl)
    # if wl['l2'] > wl['l1']:
    #     bbs_list = models.BBS.objects.order_by('bbs_category')
    # else:
    #     bbs_list = models.BBS.objects.order_by('-bbs_category')
    bbs_list = models.BBS.objects.filter(bbs_category_id=2)
    bbs_categories = models.Category.objects.all()
    bbs_user = models.BBS_user.objects.all()
    bbs_id = 0
    user = request.user
    return render(request,'technology.html',locals())

def hot(request):
    n = 0
    # 取出bbs的类别
    author = models.BBS_user.objects.get(user__username=request.user)
    wl = author.user_bbs_id
    bbs_list = models.BBS.objects.order_by('view_count')
    bbs_categories = models.Category.objects.all()
    bbs_user = models.BBS_user.objects.all()
    bbs_id = 0
    user = request.user
    return render(request,'hot.html',locals())

def home(request,u):

    user=models.BBS_user.objects.get(user__username=u)
    item=models.BBS.objects.filter(author=user).order_by('created_at')
    user=request.user
    return render(request,'home.html',locals())

def homehot(request,u):

    user=models.BBS_user.objects.get(user__username=u)
    item=models.BBS.objects.filter(author=user).order_by('view_count')
    user=request.user
    return render(request,'home.html',locals())