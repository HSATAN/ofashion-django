#-*- coding:utf-8 -*-
from django.conf.urls import url, patterns

urlpatterns = patterns(
    'tags.views',
    # url(r'^/$','tags',name='tags'),
    url(r'^/tags$','custom_tags',name='custom_tags'),
    url(r'^/gender','gender',name='gender'),
    url(r'/tags_manage', 'tags_manage', name='tags_manage'),
    url(r'/manage', 'manage', name='manage'),
    url(r'/mapping$', 'mapping', name='mapping'),
    url(r'/mapping/(?P<brand>\d*)$', 'mapping', name='mapping1'),
    url(r'/record', 'record', name='record'),
    url(r'^/mapping_ajax$', 'mapping_ajax', name='mapping_ajax'),
    url(r'^/$','tags',name='tags'),

)