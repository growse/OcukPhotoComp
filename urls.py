from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^cp/photocomp/bulkadd/$','photocomp.admin_views.bulkadd'),
    (r'^cp/photocomp/uploadimagezip/$','photocomp.admin_views.uploadimagezip'),
    (r'^cp/', include(admin.site.urls)),
    (r'^seasons/(?P<season_name>.+)/$', 'photocomp.views.season'),
    (r'^rounds/(?P<season_name>.+)/(?P<round_theme>.+)/$', 'photocomp.views.round'),
    (r'^people/(?P<person_name>.+)/$', 'photocomp.views.person'),
    (r'^search/(?P<term>.+)/$','photocomp.views.search'),
    (r'^search/$','photocomp.views.search'),
    (r'^searchhelper/(?P<term>.+)/$','photocomp.views.search',{'helper':True}),
    (r'^$','photocomp.views.season'),
)
