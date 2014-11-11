from django.conf.urls import include, patterns, url
from django.contrib import admin
from .views import test_home

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', test_home),
)
