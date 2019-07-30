from django import forms

from patlaks.choices import GENDER_CHOICES


class GetCompetitorForm(forms.Form):
    startDate = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
               'onkeydown': 'return false'}))
    endDate = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'off',
               'onkeydown': 'return false'}))

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="", initial='',
                               widget=forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                          'style': 'width: 200px;'}), )
