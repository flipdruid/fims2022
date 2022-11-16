from django.urls import path, re_path as url
from django.views.static import serve
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'clients'
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', views.index, name='index'),
    path('search',views.search, name='search'),
    path('addclient',views.addclient, name='addclient'),
    path('cancelledclient',views.cancelledclient, name='cancelledclient'),
    path('processaddclient',views.processaddclient, name='processaddclient'),
    path('<int:profile_id>/clientdetail/',views.clientdetail, name='clientdetail'),
    path('<int:profile_id>/cancelledclientdetail/',views.cancelledclientdetail, name='cancelledclientdetail'),
    # path('<int:profile_id>/clientdelete/',views.clientdelete, name='clientdelete'),
    path('<int:profile_id>/clientdisable/',views.clientdisable, name='clientdisable'),
    path('<int:profile_id>/clientedit/',views.clientedit, name='clientedit'),
    path('<int:profile_id>/processclientedit/',views.processclientedit, name='processclientedit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)