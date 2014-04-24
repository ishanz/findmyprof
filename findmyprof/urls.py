from django.conf.urls import patterns, include, url

from django.contrib import admin
from search import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'findmyprof.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'), # take care of index URL
    url(r'^search/$', views.search, name='search'), # take care of search query page
)
