# coding=utf-8
from django.db import models
from tinymce.models import HTMLField


# 用户模型
class UserInfo(models.Model):
    nickname = models.CharField(max_length=10)
    password = models.CharField(max_length=40)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=11, default='')
    # 收件人
    shou_people = models.CharField(max_length=10, default='')
    # 收货地址,省,市,县,具体地址
    p_c_a_detail = models.CharField(max_length=100, default='')
    # 邮编
    zip_code = models.IntegerField(default=0)


# 商品分类
class GoodsCategory(models.Model):
    title = models.CharField(max_length=10)
    # 封面
    cover = models.ImageField(upload_to='category')
    # css 类名
    className = models.CharField(max_length=10, default='')
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8')


# 商品
class GoodsInfo(models.Model):
    name = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='goods')
    # 单位
    unit = models.CharField(default='500g', max_length=20)
    # 点击数,热度
    click = models.IntegerField(default=0)
    # 简介
    intro = models.CharField(max_length=200)
    number = models.IntegerField(default=0)
    # 介绍
    content = HTMLField()
    # 分类
    category = models.ForeignKey(GoodsCategory)
    # 价格
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 推荐
    isTop = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name.encode('utf-8')


# 首页banner
class Banner(models.Model):
    title = models.CharField(max_length=20)
    banner = models.ImageField(upload_to='banner')
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.title.encode('utf-8')


# 订单表
class OrderInfo(models.Model):
    # 订单号
    id = models.CharField(max_length=30, primary_key=True)
    # 用户
    user = models.ForeignKey(UserInfo)
    # 日期
    date = models.DateTimeField(auto_now=True)
    # 是否支付
    isPay = models.BooleanField(default=False)
    # 支付金额
    totalPrice = models.DecimalField(max_digits=6, decimal_places=2)
    # 收货地址
    address = models.CharField(max_length=100, default='')


# 订单详情表
class OrderDetail(models.Model):
    # 商品
    goods = models.ForeignKey(GoodsInfo)
    # 订单
    order = models.ForeignKey(OrderInfo)
    # 单价
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 数量
    number = models.IntegerField(default=0)


# 购物车
class ShopCart(models.Model):
    user = models.ForeignKey(UserInfo)
    good = models.ForeignKey(GoodsInfo)
    number = models.IntegerField(default=0)
