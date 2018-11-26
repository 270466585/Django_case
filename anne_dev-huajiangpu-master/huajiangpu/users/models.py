from django.db import models
from db.AbstractModel import *
from utils.wrapper import *

# Create your models here.


class UserManager(models.Manager):

    def user_register(self, request):
        user = User()
        user.u_name = post(request, 'username')
        user.u_pass = password_encryption(post(request, 'userpass'))
        user.save()

    def user_update_recv(self, request):
        pass


class User(BaseModel):
    u_name = models.CharField(max_length=20)
    u_pass = models.CharField(max_length=80)
    u_addr = models.CharField(max_length=50)
    u_recv = models.CharField(max_length=20)
    u_tele = models.CharField(max_length=11)
    u_recv_tele = models.CharField(max_length=11)

    objects = UserManager()


