#_*_coding:utf-8_*_
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Release(models.Model):
    id = models.AutoField(primary_key=True)
    release = models.CharField(max_length=128)
    type_list = models.CharField(max_length=20)
    date = models.DateTimeField(editable=True,blank=True,auto_now_add=True)

    class Meta:
        verbose_name = '发布记录'
        verbose_name_plural = "发布记录"
    def __unicode__(self):
        return self.release

class YourAdmin(admin.ModelAdmin):
    list_display = ('release','date','type_list')
    ordering = ('date',)
    search_fields = ('date',)
    list_filter = ('date',)
admin.site.register(Release,YourAdmin)

class lvsmodify(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=56)
    password = models.CharField(max_length=128)
    IP = models.CharField(max_length=56)
    IntranetIP = models.CharField(max_length=56)
    ScriptLocation = models.CharField(max_length=128)
    onegroup = models.CharField(max_length=256)
    twogroup = models.CharField(max_length=256)
    Intranetonegroup = models.CharField(max_length=256)
    Intranettwogroup = models.CharField(max_length=256)
    Remark  = models.TextField(max_length=256,null=True,blank=True)
class lvsAdmin(admin.ModelAdmin):
    list_display = ('username','password','IP')
    list_filter = ('username',)
admin.site.register(lvsmodify,lvsAdmin)

class jenkinsmodify(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=56)
    password = models.CharField(max_length=128)
    UrlLocation = models.CharField(max_length=128)
    Remark  = models.TextField(max_length=256,null=True,blank=True)
class jenkinsAdmin(admin.ModelAdmin):
    list_display = ('username','password','UrlLocation')
    list_filter = ('username',)
admin.site.register(jenkinsmodify,jenkinsAdmin)

class publishmodify(models.Model):
    id = models.AutoField(primary_key=True)
    onegroup = models.CharField(max_length=256)
    twogroup = models.CharField(max_length=256)
    Remark  = models.TextField(max_length=256,null=True,blank=True)
class publishAdmin(admin.ModelAdmin):
    list_display = ('onegroup','twogroup','Remark')
admin.site.register(publishmodify,publishAdmin)

class hostshmodify(models.Model):
    id = models.AutoField(primary_key=True)
    IP = models.CharField(max_length=56)
    username = models.CharField(max_length=56)
    password = models.CharField(max_length=128)
    onegroup = models.CharField(max_length=256)
    twogroup = models.CharField(max_length=256)
    reductionone = models.CharField(max_length=256)
    reductiontwo = models.CharField(max_length=256)
    Remark  = models.TextField(max_length=256,null=True,blank=True)
class hostsAdmin(admin.ModelAdmin):
    list_display = ('onegroup','twogroup','Remark')
admin.site.register(hostshmodify,hostsAdmin)