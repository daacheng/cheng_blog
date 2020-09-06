from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from .feeds import AllPostRssFeed

app_name = 'blog_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>', views.ArchiveView.as_view(), name='archive'),
    path('categorys/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('categorys/', views.category, name='categorys'),
    path('tags/<int:pk>', views.TagView.as_view(), name='tag'),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'all/rss/', AllPostRssFeed(), name='rss'),
    path('search/', views.search, name='search'),
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)