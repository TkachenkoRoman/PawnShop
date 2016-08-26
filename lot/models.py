# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from user_app.models import User

class Category(models.Model):
    class Meta():
        db_table = 'Category'
        verbose_name = u"Категории"
        verbose_name_plural = u"Категории"

    Category_name = models.CharField("Заголовок категории", max_length = 200)
    Category_details = models.TextField("Описание", blank = True)
    Category_date = models.DateTimeField("Дата создания")
    Category_publick = models.BooleanField("Опубликовано?", default = False)
    Category_icon = models.ImageField("Изображение категории", upload_to = "Category_pic")

    def __unicode__(self):
        return u'%s' % (self.Category_name)

class Lot(models.Model):
    class Meta():
        db_table = 'Lot'
        verbose_name = u"Лот"
        verbose_name_plural = u"Лоты"

    options_lot_state = (
        ('NW', 'Новое'),
        ('NG', 'Новое, еще на гарантии'),
        ('BU', 'Б/У, есть потертости'),
        ('BB', 'Б/У, состояние плохое'),
        ('BD', 'Б/У, частично неработоспособно'),
        ('NB', 'Не исправно'),
        ('NZ', 'Не исправно, на зап. части'),
        )

    Lot_title = models.CharField("Заголовок", max_length = 200)
    Lot_details = models.TextField("Описание")
    Lot_main_icon = models.ImageField("Главное изображение", upload_to = "Lot_pic", blank = True)
    Lot_date = models.DateTimeField("Дата создания", blank = True)
    Lot_shortName = models.CharField("короткий заголово лота", max_length = 200, blank = True)
    Lot_price = models.IntegerField("Цена лота", default = 0)
    Lot_Category = models.ForeignKey(Category, verbose_name = u'Категория')
    Lot_publick = models.BooleanField("Опубликовано", default = False, blank = True)
    Lot_discount = models.BooleanField("Скидка", default = False)
    Lot_popular = models.BooleanField("Популярное", default = False)
    Lot_end = models.BooleanField("Завершено", default = False, blank = True)
    Lot_like = models.IntegerField("Понравилось", default = 0)
    Lot_state = models.CharField(max_length = 2, choices = options_lot_state, verbose_name = 'Состояние')
    User_creator = models.ForeignKey(User, verbose_name='Создатель лота')
    Lot_viewv = models.IntegerField(verbose_name = "Просмотров", default = 0)

    def __unicode__(self):
        return u'%s' % (self.Lot_main_icon)
        
    def __unicode__(self):
        return u'%s' % (self.Lot_title)


class Lot_pic(models.Model):
    class Meta():
        db_table = 'Lot_pic'
        verbose_name = u"фото лота"
        verbose_name_plural = u"фото лотов"

    LotPic_title = models.CharField("Заголовок", max_length = 200, blank = True)
    LotPic_img = models.ImageField("изображение", upload_to = "Lot_pic", blank = True)
    LotPic_obj = models.ForeignKey(Lot)

    def __unicode__(self):
        return u'%s' % (self.LotPic_title)

class Comments_Lot(models.Model):
    class Meta():
        db_table = 'comments'
        verbose_name = u"коментарий лота"
        verbose_name_plural = u"коментарии лотов"

    comments_text = models.TextField(verbose_name = "Текст комментария")
    comments_autor = models.CharField(max_length = 70, verbose_name = 'Имя автора')
    comments_autor_email = models.EmailField(verbose_name = 'Email', blank = True)
    comments_for_lot = models.ForeignKey(Lot)

    def __unicode__(self):
        return u'%s' % (self.comments_for_lot)
