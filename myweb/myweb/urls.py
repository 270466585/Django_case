"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog.views import index, article,about, post, xuser, editarticle, addarticle, PersonalCenter, do_login, do_logout, do_register
from blog.admin import admin_site
urlpatterns = [
    url(r'^$',index,name = 'index'),
    url(r'^index', index, name='index'),
    url(r'^article',article,name = 'article'),
    url(r'^about', about, name='about'),
    url(r'^detail/(?P<p_id>[0-9]+)/$', post ),
    url(r'^xuser/', xuser),
    url(r'^editarticle/(?P<p_id>[0-9]+)/$', editarticle),
    url(r'^addarticle/', addarticle),
    url(r'^PersonalCenter/', PersonalCenter),
    url(r'^login/', do_login),
    url(r'^logout/', do_logout),
    url(r'^register/', do_register),
    url(r'^admin/', admin_site.urls),
]
