# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class project_model(models.Model):
    projectName = models.CharField(max_length=255)
    projectGuid = models.CharField(max_length=255)
    projectUrl = models.CharField(max_length=255)
    class Meta:
        db_table = "app1_project"

class plan_model(models.Model):
    planName = models.CharField(max_length=255)
    planGuid = models.CharField(max_length=255)
    projectGuid = models.CharField(max_length=255)
    isMail = models.CharField(max_length=255)
    isReport = models.CharField(max_length=255)
    isBeautiful = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    isApp = models.CharField(max_length=255)
    class Meta:
        db_table = "app1_plan"

class turn_model(models.Model):
    turnName = models.CharField(max_length=255)
    turnGuid = models.CharField(max_length=255)
    planGuid = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    tester = models.CharField(max_length=255)
    startTime = models.DateField(max_length=255)
    endTime = models.DateField(max_length=255)
    workHour = models.CharField(max_length=255)
    mark = models.CharField(max_length=255)
    class Meta:
        db_table = "app1_turn"