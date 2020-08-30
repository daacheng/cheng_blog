from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


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


class Post(models.Model):
    title = models.CharField('标题', max_length=100)
    body = models.TextField('正文')
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    modify_time = models.DateTimeField('修改时间', default=timezone.now)
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 某个分类删除后，该分类下的所有文章也被删除
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 复写父类方法，每次保存时调用
        self.modify_time = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_app:detail', kwargs={'pk': self.pk})