from django import template
from ..models import Post, Tag, Category

register = template.Library()

"""
    自定义模板标签
"""


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
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('blog_app/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }