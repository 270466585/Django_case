from django.contrib import admin
from .models import *


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ['adv_title', 'adv_subtitle', 'adv_detail', 'adv_image1', 'adv_image2', 'adv_image3']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['g_name', 'g_cate', 'g_unit', 'g_price', 'g_look', 'g_desc', 'g_detail', 'g_image', 'g_florid']
