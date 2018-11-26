# -*- coding: utf-8 -*-


# Register your models here.

from django.contrib import admin
from blog import models
from django.contrib.auth.admin import UserAdmin  # 从django继承过来后进行定制
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # admin中涉及到的两个表单


from pagedown.widgets import AdminPagedownWidget
from django import forms

# class User_exAdmin(admin.ModelAdmin):  # 验证码部分展示
#     list_display = ('valid_code', 'valid_time', 'email')

class GlobalSettings(admin.AdminSite):
    site_title = '欢迎登录后台管理'
    site_header = 'WangShi博客'
    index_title = 'WangShi'

admin_site = GlobalSettings()


# custom user admin
class MyUserCreationForm(UserCreationForm):  # 增加用户表单重新定义，继承自UserCreationForm
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = True   # 为了让此字段在admin中为必选项，自定义一个form
        self.fields['username'].required = True  # 其实这个name字段可以不用设定required，因为在models中的MyUser类中已经设定了blank=False，但email字段在系统自带User的models中已经设定为
        # email = models.EmailField(_('email address'), blank=True)，除非直接改源码的django（不建议这么做），不然还是自定义一个表单做一下继承吧。


class MyUserChangeForm(UserChangeForm):  # 编辑用户表单重新定义，继承自UserChangeForm
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = True


class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
        self.search_fields = ('username','email',)
        self.form = MyUserChangeForm  #  编辑用户表单，使用自定义的表单
        self.add_form = MyUserCreationForm  # 添加用户表单，使用自定义的表单
        # 以上的属性都可以在django源码的UserAdmin类中找到，我们做以覆盖

    # def changelist_view(self, request, extra_context=None):  # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同
    #     if not request.user.is_superuser:  # 非super用户不能设定编辑是否为super用户
    #         self.fieldsets = ((None, {'fields': ('username', 'password',)}),
    #                           (_('Personal info'), {'fields': ('email',)}),  # _ 将('')里的内容国际化,这样可以让admin里的文字自动随着LANGUAGE_CODE切换中英文
    #                           (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
    #                           (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    #                           )  # 这里('Permissions')中没有'is_superuser',此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
    #         self.add_fieldsets = ((None, {'classes': ('wide',),
    #                                       'fields': ('username', 'password1', 'password2', 'email', 'is_active',
    #                                                  'is_staff', 'groups',),
    #                                       }),
    #                               )  #此字段定义UserCreationForm表单中的具体显示内容
    #     else:  # super账户可以做任何事
    #         self.fieldsets = ((None, {'fields': ('username', 'password',)}),
    #                           (_('Personal info'), {'fields': ('email',)}),
    #                           (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    #                           (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    #                           )
    #         self.add_fieldsets = ((None, {'classes': ('wide',),
    #                                       'fields': ('username', 'password1', 'password2', 'email', 'is_active',
    #                                                  'is_staff', 'is_superuser', 'groups'),
    #                                       }),
    #                               )
    #     return super(CustomUserAdmin, self).changelist_view(request, extra_context)



class PostForm(forms.ModelForm):
    body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = models.Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostForm

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)


    def changelist_view(self, request, extra_context=None):

        if not request.user.is_superuser:
            self.list_display = ['title','user','status']
            self.search_fields = ['title','status']
            self.readonly_fields = ['id','date_publish','status','user']
            self.exclude = ['click_count']

        else:
            self.list_display = ['title', 'user', 'status']
            self.search_fields = ['title', 'status']

        return super(PostAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.status = '0'
            obj.user = request.user
            obj.save()
        else:
            obj.save()
            # print(request.user)

        # return super(PostAdmin, self).save_model(self, request, obj, form, change)




admin_site.register(models.User, CustomUserAdmin)  # 注册一下
# admin.site.register(models.User_ex, User_exAdmin)
admin_site.register(models.Post,PostAdmin)