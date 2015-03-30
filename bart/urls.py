from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import home, etd_data

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^api$', etd_data, name='api'),
)
