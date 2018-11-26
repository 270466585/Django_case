# coding:utf-8
import logging

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.shortcuts import render, redirect
from django.conf import settings
from django.db import connection
from django.db.models import Count
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from models import *
from forms import *

logger = logging.getLogger('blog.views')

# Create your views here.
# 在这里设置全局变量，代码重构
def global_setting(request):
    # 站点基本信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    WEIBO_SINA = settings.WEIBO_SINA
    WEIBO_TENCENT = settings.WEIBO_TENCENT
    PRO_RSS = settings.PRO_RSS
    PRO_EMAIL = settings.PRO_EMAIL
    # 分类信息获取（导航数据）
    category_list = Category.objects.all()[:6]
    # 自定义Manager管理器,在models内定义,实现归档,文章归档数据
    archive_list = Article.objects.distinct_date()
    # 标签云数据
    tag_list = Tag.objects.all()
    # 广告数据（待完成）
    # 标签数据（待完成）
    # 友情链接（待完成）
    # 友情链接数据
    links_list = Links.objects.all()
    # 文章排行 (待完成）
    # 1、评论排行
    # 评论数使用了count聚合函数
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    # 2、浏览排行
    article_click_count_list = Article.objects.all().order_by()
    # 3、站长推荐
    recommended_article_list = Article.objects.filter(is_recommend=True).order_by('-clik_count')
    return locals()
# 定义主页操作
def index(request):
    try:
        # file = open('sss.txt', 'r')
        # 分类信息获取（导航数据）
        # category_list = Category.objects.all()[:6]
        #广告数据（待完成）
        # 最新文章数据
        article_list = getPage(request,Article.objects.all())
        # 文章归档
        # 1、先去获取到文章中有的年份-月份
        # print Article.objects.values('date_publish').distinct()
        # 直接使用游标取重复出现的数据，但是在做数据迁移时会出现问题，需要用django封装的模块操作
        # cursor = connection.cursor()
        # cursor.execute("SELECT DISTINCT DATE_FORMAT(date_publish, '%Y-%m') as col_date FROM blog_article ORDER BY date_publish")
        # row = cursor.fetchall()
        # print row
        # 自定义Manager管理器,在models内定义,实现归档，
        # 首先要自定义一个管理器取出同一年份月份的文章存入一个列表，这部分已被移入全局变量，无论在哪个页面都显示归档信息
        # archive_list = Article.objects.distinct_date()
    except Exception as e:
        logger.error(e)
    # 响应目标页
    return render(request, 'index.html', locals())
    # return render(request, 'index.html', {'category_list':category_list})
# 定义归档页操作
def archive(request):
    try:
        # 分类信息获取（导航数据）
        category_list = Category.objects.all()[:6]
        # 自定义Manager管理器,在models内定义,实现归档
        archive_list = Article.objects.distinct_date()
        # 先获取客户端提交的信息
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list = getPage(request,article_list)
    except Exception as e:
        logger.error(e)
    return render(request,'archive.html',locals())


# print '11111111111111111111111111'
# print Article.objects.values('tag')
def tag(request):
    try:
        tag_id = request.GET.get("tag_id",None)
        tag = Tag.objects.get(pk=tag_id)
        article_list=Article.objects.filter(tag=tag)
        article_list=getPage(request,article_list)
    except Exception as e:
        logger.error(e)
    return render(request,'tag.html',locals())
# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else {'article': id})

        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'article.html', locals())
# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           # url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request,user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())
# 分页代码封装
def getPage(request,article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list