from django.urls import path, re_path as url
from django.views.static import serve
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'mmaptsp2'
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', views.index, name='index'),    
    path('cancelledmmap', views.cancelledmmap, name='cancelledmmap'),   
    path('loadclient', views.loadclient, name='loadclient'),
    path('search', views.search, name='search'),
    path('searchclient',views.searchclient, name='searchclient'),
    path('<int:profile_id>/addmmap', views.addmmap, name='addmmap'),
    path('<int:profile_id>/mmapdetail/',views.mmapdetail, name='mmapdetail'),
    path('<int:mmap_id>/mmapedit/',views.mmapedit, name='mmapedit'),
    # path('<int:mmap_id>/mmapdelete/',views.mmapdelete, name='mmapdelete'),
    path('<int:mmap_id>/mmapcancel/',views.mmapcancel, name='mmapcancel'),
    path('<int:mmap_id>/processmmapedit/',views.processmmapedit, name='processmmapedit'),
    path('processaddmmap', views.processaddmmap, name='processaddmmap'),
    path('patchbenmmapid', views.patchbenmmapid, name='patchbenmmapid'),
    path('patchsccn', views.patchsccn, name='patchsccn'),
    path('filterby', views.filterby, name='filterby'),
    path('processfilterby', views.processfilterby, name='processfilterby'),
    path('allexpcurrent/<str:exporcurrent>/', views.allexpcurrent, name='allexpcurrent'),
    path('<int:profile_id>/mmapexpdetail/',views.mmapexpdetail, name='mmapexpdetail'),
    path('allexpcurrentexportdata/<str:exporttype>/', views.allexpcurrentexportdata, name='allexpcurrentexportdata'),
    path('exportdata/<str:exporttype>',views.exportdata, name='exportdata'),
    path('csv-upload/',views.csv_upload, name='csv_upload'),
    path('mmapclaim/',views.mmapclaim, name='mmapclaim'),
    path('newrenewstatus/',views.newrenewstatus, name='newrenewstatus'),
    path('<int:profile_id>/mmapdetailpdf/',views.mmapdetailpdf, name='mmapdetailpdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)