# -*- coding: utf-8 -*-

from user_app.models import User, messages, obj_for_rate
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _


			#--------------Пользователи-----------------


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('User info: '), {'fields': (
            'organization_name',
            'first_name',
            'last_name',
            'email',
            'org_pic',
            'description',
        )}),
        (_('Requisites: '), {'fields': ('adress', 'telephone', 'requisits',)}),
        (_('Rights: '), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates: '), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )



    		#--------------Пользователи-----------------

    		#---------------Сообщения------------------

class messagesAdmin(admin.ModelAdmin):
	fields = [
        'mess_Recipient', 
        'mess_from', 
        'message_subject', 
        'message_content', 
        'message_ReadUnread',
        ]
	list_filter = [
        'message_ReadUnread',
        ]
	list_display = (
        'mess_Recipient', 
        'mess_from', 
        'message_ReadUnread'
        )
	list_per_page = 100



    		#---------------Сообщения------------------

            #---------------Для оценки------------------

class obj_for_rateAdmin(admin.ModelAdmin):
    fields = [
        'obj_title', 
        'obj_description', 
        'obj_state', 
        'obj_pic_1', 
        'obj_pic_2', 
        'obj_pic_3', 
        'obj_date_added', 
        'obj_desired_price',
        ]
    list_filter = [
        'obj_state', 
        'obj_desired_price',
        ]
    list_display = (
        'obj_title', 
        'obj_state', 
        'obj_date_added', 
        'obj_desired_price',
        )
    list_per_page = 100

            #---------------Для оценки------------------




admin.site.register(User, UserAdmin)
admin.site.register(messages, messagesAdmin)
admin.site.register(obj_for_rate, obj_for_rateAdmin)
