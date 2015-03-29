from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import etd_data

urlpatterns = patterns('',
    url(r'^api$', etd_data, name='api'),
)
