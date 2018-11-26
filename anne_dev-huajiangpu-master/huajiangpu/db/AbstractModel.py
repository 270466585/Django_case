# coding=utf-8
from django.db import models


# 项目中所有数据模型类的基类
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    logic_delete = models.BooleanField(default=False)

    class Meta():
        abstract = True