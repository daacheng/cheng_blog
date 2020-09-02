from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include

app_name = 'blog_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>', views.archive, name='archive'),
    path('categorys/<int:pk>', views.category, name='category'),
    path('tags/<int:pk>', views.tag, name='tag'),
    url(r'mdeditor/', include('mdeditor.urls')),
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)