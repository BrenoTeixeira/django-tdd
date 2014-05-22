from django.conf.urls import patterns, url

from user_contacts.views import *


urlpatterns = patterns('',
    url(r'^$', home)        
)
