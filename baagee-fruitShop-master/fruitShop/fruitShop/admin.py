# coding=utf-8
from django.contrib import admin
from models import *


#
# class GoodsInline(admin.StackedInline):
#     model = GoodsInfo
#     extra = 3


# 商品分类
class GoodsCategoryAdmin(admin.ModelAdmin):
    # 列表显示列
    list_display = ['title', 'id', 'isDelete']
    # 搜索字段
    search_fields = ['title']
    # 右侧
    list_filter = ['title']
    # 每页条数
    list_per_page = 10
    # 添加修改分类可以直接添加对应的商品
    # inlines = [GoodsInline]


# 商品表
class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['name']
    list_filter = ['name']
    list_display = ['name', 'id', 'click', 'number', 'price','category', 'isDelete']


# 首页banner
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'url']
    list_filter = ['title']
    search_fields = ['title']


admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(Banner,BannerAdmin)
