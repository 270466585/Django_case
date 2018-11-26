from django.db import models
from django.contrib.auth.models import User
from django_comments import models as comments_models

# Create your models here.

class BBS(models.Model):
    url=models.CharField(max_length=1024,blank=True)
    title=models.CharField(max_length=64)
    summary=models.CharField(max_length=128,blank=True,null=True)
    content=models.TextField()
    author=models.ForeignKey('BBS_user')
    bbs_category=models.ForeignKey('Category',null=True)
    love_count=models.IntegerField(default=0)
    say_count=models.IntegerField(default=0)
    picture=models.ImageField(upload_to="bbs_pictrue/",default='bbs_pic.jpg',null=True)
    view_count=models.IntegerField(default=0)
    ranking=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class New(models.Model):
    u=models.CharField(max_length=10,default='cb')
    key=models.IntegerField(default=0)
    start_time=models.IntegerField(default=0)
    end_time=models.IntegerField(default=0)
    def __str__(self):
        return self.u

class Category(models.Model):
    name=models.CharField(max_length=32,unique=True)
    administrator=models.ForeignKey('BBS_user')
    def __str__(self):
        return self.name

class BBS_user(models.Model):
    user=models.OneToOneField(User)
    user_bbs_id=models.CharField(max_length=1024,default=None,null=True)
    signature=models.CharField(max_length=128,default='这个家伙很懒，什么都没留下。')
    photo=models.ImageField(upload_to="static/upload_img/",default="/static/upload_img/user_1.jpg")

    def __str__(self):
        return self.user.username
#解决中文报错
#alter table junge_bbs_user MODIFY COLUMN photo varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;