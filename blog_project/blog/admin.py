# coding:utf-8
from django.contrib import admin
from models import *
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','desc','click_count',)
    list_display_links = ('title','desc','click_count',)
    # fields\exclude
    # fieldsets
    # list_display
    # list_display_links
    # list_editable
    # list_filter
    # inlines
    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content', )
        }),
        ('高级设置', {
            'classes': ('collapse',),
            'fields': ('user', 'is_recommend', )
        }),
    )

    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Ad)
admin.site.register(Links)