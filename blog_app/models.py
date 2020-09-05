from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from mdeditor.fields import MDTextField
import markdown
import re
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.utils.functional import cached_property


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


def generate_rich_content(value):
    # markdown转html
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    content = md.convert(value)
    # 自动生成文章目录 如果没有目录，则不显示
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ''
    return {'content': content, 'toc': toc}


class Post(models.Model):
    title = models.CharField('标题', max_length=100)
    body = MDTextField('正文')
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    modify_time = models.DateTimeField('修改时间', default=timezone.now)
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 某个分类删除后，该分类下的所有文章也被删除
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)  # 浏览量

    @cached_property
    def rich_content(self):
        # cached_property将方法转为属性，以属性的方式获取方法的返回值，同时将返回值缓存起来
        return generate_rich_content(self.body)

    @property
    def toc(self):
        return self.rich_content.get('toc', '')

    @property
    def body_html(self):
        return self.rich_content.get('content', '')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # 默认是按照时间排序
        ordering = ['-create_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 复写父类方法，每次保存时调用
        self.modify_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_app:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])