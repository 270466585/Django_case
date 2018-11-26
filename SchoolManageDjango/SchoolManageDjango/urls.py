"""SchoolManageDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),


    # ---------------------------------班级管理---------------------------------


    url(r'^show_class/', views.show_class),
    url(r'^add_class/', views.add_class),
    url(r'^edit_class/', views.edit_class),
    url(r'^del_class/', views.del_class),
    url(r'^modal_add_class/', views.modal_add_class),
    url(r'^modal_edit_class/', views.modal_edit_class),
    url(r'^alert_del_class/', views.alert_del_class),


    # ---------------------------------教师管理---------------------------------


    url(r'^show_teacher/', views.show_teacher),
    url(r'^add_teacher/', views.add_teacher),
    url(r'^edit_teacher/', views.edit_teacher),
    url(r'^del_teacher/', views.del_teacher),
    url(r'^modal_add_teacher/', views.modal_add_teacher),
    url(r'^modal_edit_teacher/', views.modal_edit_teacher),
    url(r'^alert_del_teacher/', views.alert_del_teacher),


    # ---------------------------------学生管理---------------------------------


    url(r'^show_student/', views.show_student),
    url(r'^add_student/', views.add_student),
    url(r'^edit_student/', views.edit_student),
    url(r'^del_student/', views.del_student),
    url(r'^modal_add_student/', views.modal_add_student),
    url(r'^modal_edit_student/', views.modal_edit_student),
    url(r'^modal_del_student/', views.modal_del_student),

]

