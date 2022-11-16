from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'aws'

urlpatterns = [
    path ('', views.index, name='index'),
    path ('addaccount/', views.addaccount, name='addaccount'),
    path ('processaddaccount/', views.processaddaccount, name='processaddaccount'),
    path ('awsaccounts/', views.awsaccounts, name='awsaccounts'),
    path ('<int:serverid>/startreserver/', views.startreserver, name='startreserver'),
    path ('<int:serverid>/stopserver/', views.stopserver, name='stopserver'),
    path ('<str:instanceid>/instancerdp/', views.instancerdp, name='instancerdp'),
    path ('ubuntuservers/', views.ubuntuservers, name='ubuntuservers'),
    path ('<int:serverid>/startreubuntuservers/', views.startreubuntuservers, name='startreubuntuservers'),
    path ('<int:serverid>/stopubuntuservers/', views.stopubuntuservers, name='stopubuntuservers'),
    path ('windowsservers/', views.windowsservers, name='windowsservers'),
    path ('<int:serverid>/startrewindowsservers/', views.startrewindowsservers, name='startrewindowsservers'),
    path ('<int:serverid>/stopwindowsservers/', views.stopwindowsservers, name='stopwindowsservers'),    
    #ubuntuservers page

    path ('<str:area>/<str:action>/startareaservers/', views.startareaservers, name='startareaservers'),
    path ('<int:stopstart>/ssallwindowsservers/', views.ssallwindowsservers, name='ssallwindowsservers'),
    # path ('<int:serverid>/winrdpaccess/', views.winrdpaccess, name='winrdpaccess'),
]
