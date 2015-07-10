from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from MainDataCollect import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DataCollect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home),
    url(r'^clicker$', views.oneclick),
    url(r'^step-clicker/(?P<UName>([A-Za-z0-9_\.-]+))/(?P<VideoName>([A-Za-z0-9\(\)_\.-]+))$', views.stepclicker ),
    url(r'^recvData$', views.recvData),
    url(r'^dataVis/(?P<UName>([A-Za-z0-9_\.-]+))/(?P<VideoName>([A-Za-z0-9\(\)_\.-]+))$', views.dataVis),
    url(r'^uploadVideo$', views.uploadVideo)

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
