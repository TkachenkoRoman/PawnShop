# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms 
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.forms.fields import DateField, ChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from models import User
from lot.models import Lot, Category, Lot_pic
import re

rows = '8'

class UserRegForm(forms.Form):

	username = forms.CharField(
		widget = forms.TextInput(attrs={'class':'form-control'}),
		label = u'*Имя пользователя ', 
		max_length = 30,
		)

	email = forms.EmailField(
		widget = forms.TextInput(attrs={'class':'form-control'}),
		label=u'*Email '
		)

	password1 = forms.CharField(
		label=u'*Пароль', 
		widget=forms.PasswordInput(attrs={'class':'form-control'})
		)

	password2 = forms.CharField(
		label=u'*Повторите ввод пароля', 
		widget=forms.PasswordInput(attrs={'class':'form-control'})
		)

	organization_name = forms.CharField(
		label=u'*Название организации', 
		widget=forms.Textarea(attrs={'class':'form-control', 'type': 'textarea', 'rows': rows}),
		)

	org_pic = forms.ImageField(
		label=u'Изображение организации', 
		required=False
		)

	adress = forms.CharField(
		label=u'*Адрес организации', 
		widget=forms.TextInput(attrs={'class':'form-control'}),
		required=False
		)

	requisits = forms.CharField(
		label=u'Реквизиты организации', 
		widget=forms.Textarea(attrs={'class':'form-control', 'type': 'textarea', 'rows': rows}),
		required=False
		)

	description = forms.CharField(
		label=u'*Описание организации', 
		widget=forms.Textarea(attrs={'class':'form-control', 'type': 'textarea', 'rows': rows}),
		required=False
		)

	telephone = forms.CharField(
		label=u'*Номер телефона организации', 
		widget=forms.TextInput(attrs={'class':'form-control'}),
		required=False
		)

	def clean_username(self):
	    username = self.cleaned_data['username']
	    if not re.search(r'^\w+$', username):
	        raise forms.ValidationError('Имя пользователя может содержать только буквы латинского алфавита, цифры и знак подчеркивания.')
	    try:
	        User.objects.get(username=username)
	    except User.DoesNotExist:
	        return username
	    raise forms.ValidationError('Пользователь с таким именем уже существует.')

	def clean_password2(self):
	    if 'password1' in self.cleaned_data:
	       password1 = self.cleaned_data['password1']
	       password2 = self.cleaned_data['password2']
	       if password1 == password2:
	           return password2
	    raise forms.ValidationError('Пароли не совпадают.')

	def clean_email(self):
	    email = self.cleaned_data['email']
	    try:
	        User.objects.get(email = email)
	    except User.DoesNotExist:
	        return email
	    raise forms.ValidationError('Пользователь с таким email уже существует.')



class User_editForm(forms.Form):

	org_pic = forms.ImageField(
		label = u'Изображение организации', 
		required = False,
		)

	email = forms.CharField(
		widget = forms.TextInput(attrs={'class':'form-control', 'value':'user_data.email'}),
		label = u'*Email ',
		)

	organization_name = forms.CharField(
		label=u'*Название организации', 
		widget=forms.TextInput(attrs={'class':'form-control'}),
		)

	adress = forms.CharField(
		label=u'*Адрес организации', 
		widget=forms.TextInput(attrs={'class':'form-control'}),
		required=False
		)

	requisits = forms.CharField(
		label=u'Реквизиты организации', 
		widget=forms.Textarea(attrs={'class':'form-control', 'type': 'textarea', 'rows': rows}),
		required=False
		)

	description = forms.CharField(
		label=u'*Описание организации', 
		widget=forms.Textarea(attrs={
			'class':'form-control', 
			'type': 'textarea', 
			'rows': rows}
			),
		required=False
		)

	telephone = forms.CharField(
		label=u'*Номер телефона организации', 
		widget=forms.TextInput(attrs={'class':'form-control'}),
		required=False,
		)

class changePasswordForm(forms.Form):

	old_password = forms.CharField(
		label=u'*Введите текущий пароль', 
		widget=forms.PasswordInput(attrs={'class':'form-control'})
		)

	password1 = forms.CharField(
		label=u'*Новый пароль', 
		widget=forms.PasswordInput(attrs={'class':'form-control'})
		)

	password2 = forms.CharField(
		label=u'*Повторите ввод пароля', 
		widget=forms.PasswordInput(attrs={'class':'form-control'})
		)

	def clean_password2(self):
	    if 'password1' in self.cleaned_data:
	       password1 = self.cleaned_data['password1']
	       password2 = self.cleaned_data['password2']
	       if password1 == password2:
	           return password2
	    raise forms.ValidationError('Пароли не совпадают.')

class add_my_lotForm(ModelForm):
    options_lot_state = (
        ('NW', 'Новое'),
        ('NG', 'Новое, еще на гарантии'),
        ('BU', 'Б/У, есть потертости'),
        ('BB', 'Б/У, состояние плохое'),
        ('BD', 'Б/У, частично неработоспособно'),
        ('NB', 'Не исправно'),
        ('NZ', 'Не исправно, на зап. части'),
        )
    class Meta:
         model = Lot
         fields = ['Lot_main_icon', 'Lot_title', 'Lot_details', 'Lot_shortName', 'Lot_price', 'Lot_Category', 'Lot_publick', 'Lot_end', 'Lot_state']
         widgets = {
            'Lot_title': forms.TextInput(attrs={'class':'form-control'}),
            'Lot_details': forms.Textarea(attrs={'class':'form-control'}),
            'Lot_shortName': forms.TextInput(attrs={'class':'form-control'}),
            'Lot_price': forms.TextInput(attrs={'class':'form-control'}),
            'Lot_Category': forms.Select(attrs={'class':'form-control'}),
            'Lot_publick': 	forms.CheckboxInput(attrs={'class':'form-control'}),
            'Lot_end': 	forms.CheckboxInput(attrs={'class':'form-control'}),
            'Lot_state': forms.Select(attrs={'class':'form-control'}, choices = 'options_lot_state'),
        }

class LotPicForm(forms.ModelForm):
    class Meta:
        model = Lot_pic
        fields = ('LotPic_title', 'LotPic_img')


#LotFormSet = inlineformset_factory(Lot, Lot_pic, fields=('LotPic_title',), can_delete = False, extra = 5)
addLotPicFormSet = formset_factory(LotPicForm, extra = 4)

class editLotForm(forms.ModelForm):
	class Meta:
		model = Lot
		fields = ['Lot_main_icon', 'Lot_title', 'Lot_details', 'Lot_shortName', 'Lot_price', 'Lot_Category', 'Lot_publick', 'Lot_end', 'Lot_state']
		widgets = {
			'Lot_main_icon': forms.FileInput(attrs={"accept": "image/jpeg,image/png,image/gif"}),
            'Lot_title': forms.TextInput(attrs={'class':'form-control'}),
            'Lot_details': forms.Textarea(attrs={'class':'form-control'}),
            'Lot_shortName': forms.TextInput(attrs={'class':'form-control'}),
            'Lot_price': forms.TextInput(attrs={'class':'form-control'}),
            'Lot_Category': forms.Select(attrs={'class':'form-control'}),
            'Lot_publick': 	forms.CheckboxInput(attrs={'class':'form-control'}),
            'Lot_end': 	forms.CheckboxInput(attrs={'class':'form-control'}),
            'Lot_state': forms.Select(attrs={'class':'form-control'}, choices = 'options_lot_state'),
        }


inline_Lot_pic_formset = inlineformset_factory(Lot, Lot_pic, fields = ('LotPic_title', 'LotPic_img',), can_delete = False, extra = 4)