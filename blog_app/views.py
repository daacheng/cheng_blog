from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Category, Tag
import markdown
import re
from django.db.models import Q
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from pure_pagination import PaginationMixin
from django.contrib import messages
from django.db.models.aggregates import Count


class IndexView(PaginationMixin, ListView):
    # 类视图
    model = Post  # 指定模型
    template_name = 'blog_app/index.html'  # 指定要渲染的页面
    context_object_name = 'post_list'  # 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板。
    paginate_by = 10


class CategoryView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        # 在类视图中，从URL捕获的路径参数值保存在实例的kwargs属性里(字典)，非路径参数值保存在实例的args属性里(列表)。
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)


class TagView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tag=tag)


class ArchiveView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(create_time__year=year, create_time__month=month)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 重写父类方法，每次访问时候执行，记录阅读量
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 重写父类方法，对返回的body进行处理
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        # 自动生成文章目录 如果没有目录，则不显示
        # m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        # post.toc = m.group(1) if m is not None else ''
        return post


def profile(request):
    context = {
        'pic_url': 'https://avatars0.githubusercontent.com/u/29137126',
        'nick_name': '大诚',
        'email': '1193685537@qq.com',
        'position': '武汉',
        'status': 'coding...',
        'website': 'http://www.daacheng.top',
        'zhihu': 'https://www.zhihu.com/people/mrxian-sheng-65',
        'github': 'https://github.com/daacheng',
    }

    return render(request, 'blog_app/profile.html', context=context)


def search(request):
    # 表单get方法提交的参数在request.GET中
    q = request.GET.get('q')
    if not q:
        error_message = '请输入搜索关键字'
        messages.add_message(request, messages.ERROR, error_message, extra_tags='danger')
        return redirect('blog_app:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog_app/index.html', context={'post_list': post_list})


def index(request):
    post_list = Post.objects.all()
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

    # 统计访问量
    post.increase_views()
    return render(request, 'blog_app/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month)
    return render(request, 'blog_app/index.html', context={'post_list': post_list})


def show_categorys(request):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return render(request, 'blog_app/categorys.html', context={'category_list': category_list})


def show_archives(request):
    archives_info = {}
    create_time_set = Post.objects.dates('create_time', 'day', order='DESC')
    for create_time in create_time_set:
        year = create_time.year
        month = create_time.month
        post_list = Post.objects.filter(create_time__year=year,
                                        create_time__month=month)
        archives_info['{}-{}'.format(year, month)] = post_list
    return render(request, 'blog_app/archives.html', context={'archives_info': archives_info})


def tag(request, pk):
    tag_ = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tag=tag_)
    return render(request, 'blog_app/index.html', context={'post_list': post_list})