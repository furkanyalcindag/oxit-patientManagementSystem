from django import forms
from django.forms import ModelForm

from patlaks.models.Message import Message


class MessageForm(forms.Form):
    body = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control ', 'placeholder': 'Mesaj İçeriği', 'required': 'required'}))

    to = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control ', 'id': 'tags', 'placeholder': 'Kullanıcı Adı'}))
