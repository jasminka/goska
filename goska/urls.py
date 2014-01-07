from django.conf.urls import patterns, include, url
from django.contrib import admin

from main import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gobcn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^coor/$', views.obcina, name='obcina'),
    url(r'^compare/$', views.prim, name='prim'),
)