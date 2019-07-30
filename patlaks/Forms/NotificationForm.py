from django import forms
from django.forms import ModelForm

from patlaks.models.Notification import Notification


class NotificationForm(ModelForm):
    # profileImage = forms.ImageField(widget=forms.ClearableFileInput(
    #   attrs={'class': 'form-control-file'}))

    class Meta:
        model = Notification
        fields = ('title', 'body')
        widgets = {
            'body': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Bildirim İçeriği', 'required': 'required'}),
            'title': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Bildirim Başlığı'}),
        }
