from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
import markdown
import re
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify


def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog_app/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    # 自动生成文章目录 如果没有目录，则不显示
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog_app/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month).order_by('-create_time')
    return render(request, 'blog_app/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog_app/index.html', context={'post_list': post_list})


def tag(request, pk):
    tag_ = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tag=tag_).order_by('-create_time')
    return render(request, 'blog_app/index.html', context={'post_list': post_list})