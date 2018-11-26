# coding=utf-8
from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    """商品类型"""
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    """商品详细信息"""
    gtitle = models.CharField(max_length=20)
    # 商品图片信息 注意配置setting.py
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    # 价格下方的单位：34元/500g
    gunit = models.CharField(max_length=20,default='500g')
    gclick = models.IntegerField()
    # 库存
    gkucun = models.IntegerField()
    # 商品详细信息 ，使用富文本编辑器
    gcontent = HTMLField()
    # 外键约束
    gtype = models.ForeignKey(TypeInfo)
    # 推荐商品
    # gadv = models.BooleanField(default=False)
