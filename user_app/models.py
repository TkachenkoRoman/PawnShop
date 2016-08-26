# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes

AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False


class User(AbstractUser):

    org_pic = models.ImageField(
    	verbose_name = 'Изображение пользователя',
    	help_text='Избражение будет отображатся в карточке!',
    	upload_to='users/avatar', 
        blank=True, 
    	)

    organization_name = models.TextField(
    	verbose_name='Название организации',
    	blank=False
    	)

    adress = models.CharField(
    	verbose_name='Адресс',
    	max_length=512,
    	help_text='Адрес организации'
    	)

    requisits = models.TextField(
    	verbose_name='Реквизиты',
    	help_text='Здесь можно указать адресс, телефон, инн и т.д.',
    	blank=True
    	)

    description = models.TextField(
    	verbose_name='Описание',
    	help_text="Описание будет видно ВСЕМ при просмотре вашей карточки!"
    	)

    telephone = models.CharField(
    	verbose_name='Номер телефона',
    	max_length=19, 
        help_text='Не обязательно для заполнения',
    	blank=True,
        )


    def __unicode__(self):
        return u'%s' % (self.username)


class messages(models.Model):
	class Meta():
		db_table = 'messages_for_user'
		verbose_name = u"Сообщения"
		verbose_name_plural = u"Сообщения"
    
	message_subject = models.CharField(
        verbose_name = 'Тема', 
        blank = True,	
        help_text = 'Необязательно для заполнения',	
        max_length = 128, 
        default = 'Тема',
        )
	message_content = models.TextField(
        verbose_name = 'Текст сообщения',
        )
	mess_Recipient = models.ForeignKey(
        User, 
        verbose_name = 'Получатель',
        )
	message_ReadUnread = models.BooleanField(
        verbose_name = 'Прочитано', 
        default = False,
        )
	mess_from = models.CharField(
        verbose_name = 'От кого', 
        max_length = 255,
        )

	def __unicode__(self):
		return u'%s' % (self.mess_Recipient)


class obj_for_rate(models.Model):
    class Meta():
        db_table = 'obj_for_rate'
        verbose_name = u"Вещи для оценки"
        verbose_name_plural = u"Вещи для оценки"

    options_obj_state = (
        ('NW', 'Новое'),
        ('NG', 'Новое, еще на гарантии'),
        ('BU', 'Б/У, есть потертости'),
        ('BB', 'Б/У, состояние плохое'),
        ('BH', 'Б/У, частично неработоспособно'),
        ('NP', 'Не исправно'),
        ('NZ', 'Не исправно, на зап. части'),
        )

    obj_title = models.CharField(
        verbose_name = 'Название', 
        max_length = 255
        )
    obj_description = models.TextField(
        verbose_name = 'Описание',
        )
    obj_state = models.CharField(
        max_length = 2, 
        choices = options_obj_state, 
        verbose_name = 'Состояние',
        )
    obj_pic_1 = models.ImageField(
        verbose_name = 'Изображение 1', 
        upload_to = "obj_static",
        )
    obj_pic_2 = models.ImageField(
        verbose_name = 'Изображение 2', 
        upload_to = "obj_static",
        )
    obj_pic_3 = models.ImageField(
        verbose_name = 'Изображение 3', 
        upload_to = "obj_static",
        )
    obj_date_added = models.DateTimeField(
        verbose_name = 'Дата создания', 
        blank = True,
        )
    obj_desired_price = models.IntegerField(
        verbose_name = 'Желаемая цена', 
        default = 0, 
        blank = True,
        )

    def __unicode__(self):
        return u'%s' % (self.obj_title)