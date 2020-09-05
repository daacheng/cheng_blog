from django.contrib.syndication.views import Feed
from .models import Post


class AllPostRssFeed(Feed):
    # 显示在聚合器上的标题
    title = '哒哒哒大大诚'
    # 通过聚合阅读器跳转到网站的地址
    link = "/"
    # 显示在聚合阅读器上的描述信息
    description = '哒哒哒大大诚 全部文章'

    def items(self):
        # 需要显示的条目
        return Post.objects.all()

    def item_title(self, item):
        # 需要显示条目的标题
        return "{}({})".format(item.title, item.category)

    def item_description(self, item):
        # 显示条目的内容
        return item.body_html