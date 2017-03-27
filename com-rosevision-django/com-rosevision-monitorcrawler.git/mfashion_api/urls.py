#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
import configurations.views
from sellers.views import get_seller_info, lookup_seller, update_seller
# from products.views import query_products
from web.views import *
import accounts.views

admin.autodiscover()

urlpatterns = patterns('',
                       # admin
                       url(r'^admin/', include(admin.site.urls)),

                       # Sellers
                       url(r'^sellers/$', update_seller),
                       url(r'^sellers/(\d+)/$', get_seller_info),
                       url(r'^sellers/query/([^/]+)/$', lookup_seller),

                       # Searches
                       # url(r'^products/searches/$', query_products),

                       # Configuration
                       url(r'^configurations/config/([^/]+)/$', configurations.views.config),
                       url(r'^configurations/hostdata/([^/]+)/$', configurations.views.host_data),

                       #account
                       url(r'^accounts/login/$', accounts.views.login_view),
                       url(r'^accounts/logout/$', accounts.views.logout_view),
                       url(r'^accounts/unauthenticated/$', accounts.views.unauthenticated_view),

                       #tags
                       url(r'^tags', include('tags.urls')),

                       #todo conflict with configure url
                       url(r'^', include('web.urls')),

)
url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
