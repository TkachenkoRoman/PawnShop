# -*- coding: utf-8 -*-

from django.contrib import admin
from lot.models import Category, Lot, Lot_pic, Comments_Lot

class Comments_LotInline(admin.StackedInline):
    model = Comments_Lot
    extra = 1
    list_per_page = 10
    max_num = 4


class Lot_PicInline(admin.StackedInline):
    model = Lot_pic
    extra = 1
    list_per_page = 10
    max_num = 8

class CategoryAdmin(admin.ModelAdmin):
    fields = ['Category_name', 'Category_details', 'Category_date', 'Category_icon', 'Category_publick']
    list_filter = ['Category_date', 'Category_publick', ]
    list_display = ('Category_name', 'Category_date', 'Category_publick')
    list_per_page = 50

class LotAdmin(admin.ModelAdmin):
    fields = ['Lot_title', 'Lot_details', 'Lot_main_icon', 'User_creator', 'Lot_state', 'Lot_date', 'Lot_shortName', 'Lot_price', 'Lot_Category', 'Lot_publick', 'Lot_discount', 'Lot_popular', 'Lot_end',]
    inlines = (Lot_PicInline, Comments_LotInline)
    list_filter = ['Lot_date', 'Lot_state', 'Lot_like', 'Lot_Category', 'Lot_publick', 'Lot_discount', 'Lot_popular', 'Lot_end']
    list_display = ('Lot_title', 'Lot_date', 'Lot_price', 'Lot_Category', 'User_creator', 'Lot_publick', 'Lot_discount', 'Lot_popular', 'Lot_end', )
    list_per_page = 50

class Comments_LotAdmin(admin.ModelAdmin):
	fields = ['comments_autor', 'comments_text', 'comments_autor_email', 'comments_for_lot',]
	list_per_page = 100

admin.site.register(Category, CategoryAdmin)
admin.site.register(Lot, LotAdmin)
admin.site.register(Comments_Lot, Comments_LotAdmin)