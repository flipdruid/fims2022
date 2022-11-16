from django.urls import re_path as url
# from django.conf import settings
from django.views.static import serve

from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'users'
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', views.index, name='index'),
    path('login',views.loginview, name='loginview'),
    path('login/process',views.process, name='process'),
    path('logout',views.processlogout, name='processlogout'),
    path('add',views.add, name='add'),
    # path('userreg',views.userreg, name='userreg'),
    path('search',views.search, name='search'),
    path('processadd',views.processadd, name='processadd'),
    path('<int:profile_id>/detail/',views.detail, name='detail'),
    path('<int:profile_id>/delete/',views.delete, name='delete'),
    path('<int:profile_id>/edit/',views.edit, name='edit'),
    path('<int:profile_id>/processedit/',views.processedit, name='processedit'),
    path('addcomment',views.addcomment, name='addcomment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)