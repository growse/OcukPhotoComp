from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^cp/photocomp/bulkadd/$','ocukphotocomp.photocomp.admin_views.bulkadd'),
    (r'^cp/photocomp/uploadimagezip/$','ocukphotocomp.photocomp.admin_views.uploadimagezip'),
    (r'^cp/', include(admin.site.urls)),
    (r'^seasons/(?P<season_name>.+)/$', 'ocukphotocomp.photocomp.views.season'),
    (r'^rounds/(?P<season_name>.+)/(?P<round_theme>.+)/$', 'ocukphotocomp.photocomp.views.round'),
    (r'^people/(?P<person_name>.+)/$', 'ocukphotocomp.photocomp.views.person'),
    (r'^search/(?P<term>.+)/$','ocukphotocomp.photocomp.views.search'),
    (r'^search/$','ocukphotocomp.photocomp.views.search'),
    (r'^searchhelper/(?P<term>.+)/$','ocukphotocomp.photocomp.views.search',{'helper':True}),
    (r'^$','ocukphotocomp.photocomp.views.season'),
)
