from django.contrib import admin
from News import models
# Register your models here.
class BBS_admin(admin.ModelAdmin):
    list_display = ('title','summary','author','bbs_category_id','signature','view_count','created_at')
    list_filter = ('created_at',)
    search_fields = ('title','author__user__username') #外键使用__线应用
    def signature(self,obj):
        return obj.author.signature
    signature.short_description = 'description'

admin.site.register(models.BBS,BBS_admin)
admin.site.register(models.Category)
admin.site.register(models.BBS_user)
admin.site.register(models.New)