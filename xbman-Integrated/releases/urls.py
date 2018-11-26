#-*- coding:utf-8 -*-
"""xbman-Integrated URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'releases.views.index'),
    url(r'^index/', 'releases.views.index'),
    url(r'^tables/', 'releases.views.tables'),
    url(r'^lvsmodify/', 'releases.views.lvsmodify'),
    url(r'^jenkinsmodify/', 'releases.views.jenkinsmodify'),
    url(r'^publishmodify/', 'releases.views.publishmodify'),
    url(r'^hostsmodify/', 'releases.views.hostshmodify'),
    url(r'^hostsoperate/', 'releases.views.hostsoperate'),
    url(r'^hostsreduction/', 'releases.views.hostsreduction'),
    url(r'^relemanager/', 'releases.views.relemanager'),
    url(r'^odline/', 'releases.views.odline'),
    url(r'^ipvsadm/', 'releases.views.ipvsadm'),
    url(r'^onrelease/', 'releases.views.onrelease'),
    url(r'^onlyrelease/', 'releases.views.onlyrelease'),
    url(r'^onlylvs/', 'releases.views.onlylvs'),
    url(r'^svnmarge/', 'releases.views.svnmarge'),
    url(r'^marge/', 'releases.views.magre'),
]
