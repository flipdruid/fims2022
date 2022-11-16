from django.contrib import admin
from django.urls import include, path, re_path as url
from django.views.static import serve
from django.conf import settings
from . import views

app_name = 'event'

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path ('', views.index, name='index'),
    path ('saveditevent/', views.saveditevent, name='saveditevent'),
    path ('delete/', views.delete, name='delete'),
    path ('edit/', views.edit, name='edit'),
    # path ('eventsetup/', views.eventsetup, name='eventsetup')
    path ('<int:eid>/eventpage/', views.eventpage, name='eventpage'),
    path ('eventpagejq/', views.eventpagejq, name='eventpagejq'),
    path ('eventpagesetup/', views.eventpagesetup, name='eventpagesetup'),

    #position
    path ('saveditpos/', views.saveditpos, name='saveditpos')
    
]
