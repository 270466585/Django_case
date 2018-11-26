# coding:utf-8
from django.urls import path,re_path
from . import views
app_name='comments'
urlpatterns=[
    re_path(r'^comments/post/(?P<post_pk>[0-9]+)/$',views.post_comment,name='post_comment'),
]
