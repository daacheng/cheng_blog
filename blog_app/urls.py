from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from .feeds import AllPostRssFeed
from django.views.static import serve
from blog.settings import MEDIA_ROOT

app_name = 'blog_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>', views.ArchiveView.as_view(), name='archive'),
    path('categorys/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('show_categorys/', views.show_categorys, name='show_categorys'),
    path('show_archives/', views.show_archives, name='show_archives'),
    path('tags/<int:pk>', views.TagView.as_view(), name='tag'),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'all/rss/', AllPostRssFeed(), name='rss'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    # 处理 media 信息，用于图片获取
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)