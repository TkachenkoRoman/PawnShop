# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from models import Comments_Lot

class CommentForm(ModelForm):
    class Meta:
        model = Comments_Lot
        fields = ['comments_autor', 'comments_autor_email', 'comments_text',]
        widgets = {
            'comments_autor': forms.TextInput(attrs={'class': 'form-control'}),
            'comments_autor_email': forms.TextInput(attrs={'class': 'form-control'}),
            'comments_text': forms.TextInput(attrs={'class': 'form-control coment_area'}),
        } 