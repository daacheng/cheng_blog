from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    # 后台管理页面显示字段
    list_display = ['name', 'email', 'url', 'post', 'create_time']
    # 后台表单页面显示字段
    fields = ['name', 'email', 'url', 'text', 'post']

    def save_model(self, request, obj, form, change):
        # 自动设置作者为当前登录用户
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Comment, CommentAdmin)
