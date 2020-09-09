from django import template
from ..models import Post, Tag, Category
from django.db.models.aggregates import Count
import time

register = template.Library()

"""
    自定义模板标签
"""


# 注册过滤器
@register.filter
def if_time_recent(time_):
    time_stamp = time.mktime(time.strptime(str(time_), '%Y-%m-%d'))
    if int(time.time() - time_stamp) > 3600 * 24:
        return None
    return time_


@register.inclusion_tag('blog_app/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-create_time')[:num]
    }


@register.inclusion_tag('blog_app/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('create_time', 'month', order='DESC')
    }


@register.inclusion_tag('blog_app/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog_app/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list
    }