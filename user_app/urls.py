# -*- coding: utf-8 -*-
from django.conf.urls import include, url

urlpatterns = [
	url(r'^dellot/(?P<lot_ids>\w+)/$', 'user_app.views.dellot'),
	url(r'^editlot/(?P<lot_ids>\d+)/$', 'user_app.views.editLot'),
	url(r'^login/$', 'user_app.views.login'),
	url(r'^logout/$', 'user_app.views.logout'),
	url(r'^register/$', 'user_app.views.register'),
	url(r'^my_messages/$', 'user_app.views.my_messages'),
	url(r'^show_profil/$', 'user_app.views.self_show_profile'),
	url(r'^edit_profile/$', 'user_app.views.edit_profile'),
	url(r'^show_me_my_lot/$', 'user_app.views.show_me_my_lot'),
	url(r'^change_password/$', 'user_app.views.change_password'),
	url(r'^show_me_my_lot/add/$', 'user_app.views.add_my_lot'),
	url(r'^show/(?P<user_id>\d+)/$', 'user_app.views.show_my_req'),



]

