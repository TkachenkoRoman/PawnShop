# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
	url(r'^show/(?P<Category_id>\d+)/$', 'lot.views.get_lots'),
	url(r'^show/show_details/(?P<Lot_id>\d+)/$', 'lot.views.get_lot_detail'),
	url(r'^commentapp/add_comment/(?P<Lot_id>\d+)/$', 'lot.views.add_comment'),	
	url(r'^search/', 'lot.views.search'),
	url(r'^', 'lot.views.main'),
]
