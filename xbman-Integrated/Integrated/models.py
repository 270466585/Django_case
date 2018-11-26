#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.db import models
from Integrated.user_models import UserProfile
# Create your models here.

class Authoritys(models.Model):
    event_type_choices = (
        ('1', u'Empowerment'),
        ('2', u'NoEmpowerment'),
    )
    user_name = models.ForeignKey(UserProfile,verbose_name=u'用户名')
    mark = models.CharField(u'权限', choices=event_type_choices, max_length=64, blank=True, null=True)
    Auth_name = models.CharField(u'app', max_length=64,blank=True)
    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = "权限表"