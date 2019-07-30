from django import forms

from patlaks.choices import GENDER_CHOICES


class CompetitorNotificationForm(forms.Form):
    startYear = forms.IntegerField(required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control ', 'value':0}))

    endYear = forms.IntegerField(required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control ',  'value':0}))

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="", initial='',required=True,
                               widget=forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                          'style': 'width: 200px;'}))

