# -*- coding: utf-8 -*-

from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

# class EditForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('id','title', 'desc','img_link','music_link','body','status','user')

# class AddForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('id','title', 'desc','img_link','music_link','body','status','user')

class EditForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '文章ID', 'required': 'required'}),
                            error_messages={'required': '文章ID不能为空'})
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '文章标题', 'required': 'required'}),
                               max_length=100, error_messages={'required': '文章标题不能为空'})
    desc = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '文章摘要', 'required': 'required'}),
                            max_length=200, error_messages={'required': '文章摘要不能为空'})
    img_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '封面图片链接', 'required': 'required'}),
                            max_length=200, error_messages={'required': '封面图片链接不能为空'})
    music_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '音乐链接', 'required': 'required'}),
                            max_length=300, error_messages={'required': '音乐链接不能为空'})
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '文章正文', 'required': 'required'}),
                            max_length=50000, error_messages={'required': '文章正文不能为空'})
    status = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '发布状态', 'required': 'required'}),
                            max_length=20, error_messages={'required': '发布状态不能为空'})
    # status = forms.ChoiceField(choices=[('0','待审核'),('1','待发布'),('2','已发布'),('3','抱歉，未通过审核')])
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '作者', 'required': 'required'}),
                            max_length=50, error_messages={'required': '作者不能为空'})





class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': '用户名','required':'required'}),
                               max_length=50,error_messages={'required':'用户名不能为空'})
    email = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': '邮箱','required':'required'}),
                            max_length=100,error_messages={'required':'邮箱不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder': '密码','required':'required'}),
                               max_length=20,error_messages={'required':'密码不能为空'})
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '确认密码', 'required': 'required'}),
                               max_length=20, error_messages={'required':'两次输入密码必须一致'})

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': '用户名','required':'required'}),
                               max_length=50,error_messages={'required':'用户名不能为空'})

    password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder': '密码','required':'required'}),
                               max_length=20,error_messages={'required':'密码不能为空'})