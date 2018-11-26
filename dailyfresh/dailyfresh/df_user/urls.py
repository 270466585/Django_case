# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^register_handle/$', views.register_handle),
    #url(r'^register(\w+)/$',views.register_check), 拦截bug
    url(r'^register_exist/$',views.register_exist),
    url(r'^register_check2/$',views.register_check2),

    url(r'^login/$',views.login),
    url(r'^login_handle/$',views.login_handle),

    url(r"^info/$",views.info),
    url(r'^order/$',views.order),
    url(r'^site/$',views.site),

]