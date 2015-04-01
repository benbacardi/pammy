'''Pammy urls'''
from django.conf.urls import patterns, url, include

from django.views.generic import TemplateView

from .api.v1 import api as v1_api

urlpatterns = patterns('',

    url(r'^$', 'pammy.views.ip_list', name='pammy/ip_list'),
    url(r'^divide/(?P<network>[\d\./]+)/$', 'pammy.views.divide', name='pammy/divide'),
    url(r'^fill/(?P<network>[\d\./]+)/$', 'pammy.views.fill', name='pammy/fill'),

    url(r'^ui/allocation-table/$', 'pammy.views.ui.allocation_table', name='pammy/ui/allocation_table'),
    url(r'^ui/split-network/$', 'pammy.views.ui.split_network', name='pammy/ui/split_network'),

    url(r'^test/$', TemplateView.as_view(template_name='pammy/test.html')),
    url(r'^test2/$', TemplateView.as_view(template_name='pammy/test2.html')),
    url(r'^api/', include(v1_api.urls)),
)
