from django.contrib import admin
from .models import Category, Tag, Post


class PostAdmin(admin.ModelAdmin):
    # 后台管理页面显示字段
    list_display = ['title', 'create_time', 'modify_time', 'category', 'author']
    # 后台表单页面显示字段
    fields = ['title', 'body', 'excerpt', 'category', 'tag']

    def save_model(self, request, obj, form, change):
        # 自动设置作者为当前登录用户
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)



