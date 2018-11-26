# coding=utf-8

from django.conf.urls import url
import views
from views import *

urlpatterns = [
    url(r'^user/register$', views.user_register, name='user_register'),
    url(r'^user/user_exist$', views.user_exist, name='user_exist'),
    url(r'^user/login$', views.user_login, name='user_login'),
    url(r'^user/info$', views.user_info, name='user_info'),
    url(r'^user/order/(\d*)$', views.user_order, name='user_order'),
    url(r'^user/site$', views.user_site, name='user_site'),
    url(r'^user/logout', views.user_logout, name='user_logout'),

    url(r'^$', views.index, name='index'),
    url(r'^list/(\d+)/(\d*)/(\d*)$', views.list, name='list'),
    url(r'^detail/(\d+)$', views.detail, name='detail'),

    url(r'^mycart$', views.cart, name='cart'),
    url(r'^addcart$', views.addCart, name='addcart'),
    url(r'^getcartcount$', views.getMyCartCount, name='getcartcount'),
    url(r'^editcart$', views.editCartGood, name='editcart'),
    url(r'^revieworder$', views.reviewOrder, name='revieworder'),
    url(r'^orderhandle$', views.orderHandle, name='orderhandle'),
    url(r'^pay/(\d+)$', views.pay, name='pay'),
    url(r'^search/',MySearchView())
]
