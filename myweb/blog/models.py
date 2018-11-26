# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):

    id = models.IntegerField(auto_created=True,primary_key=True)
    email =models.CharField(max_length=150,unique=True,verbose_name='邮箱')
    username = models.CharField(max_length= 128, unique=True,verbose_name='用户名')
    about_me = models.CharField(max_length= 800,verbose_name='关于')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username


class Post(models.Model):

    id = models.IntegerField(auto_created=True,primary_key=True)
    title = models.CharField(max_length=500,verbose_name='文章标题')
    desc = models.CharField(max_length=200,verbose_name='文章摘要')
    img_link = models.CharField(max_length=800,verbose_name='封面图片链接')
    music_link = models.CharField(max_length=1000,verbose_name='音乐链接')

    body = models.TextField(max_length=5000000,verbose_name='文章内容')

    click_count = models.IntegerField(default=0,verbose_name='点击次数')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    status = models.CharField(max_length=2,choices=(('0',u'待审核'), ('1',u'待发布'), ('2',u'已发布'), ('3','抱歉,未通过审核')),verbose_name='发布状态')
    user = models.ForeignKey(User,verbose_name='用户')


    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']


    def __unicode__(self):
        return self.title