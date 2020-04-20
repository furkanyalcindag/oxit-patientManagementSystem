from django import forms
from django.forms import ModelForm

from booqe.models import Blog, Category


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'blog','description', 'categories', 'tags', 'isPublish')

        widgets = {

            'blog': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Blog', 'rows': '10', 'required': 'required'}),

            'description': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Özet', 'rows': '5', 'required': 'required'}),

            'title': forms.TextInput(
                attrs={'class': 'form-control ',  'placeholder': 'Blog Başlığı'}),

            'tags': forms.TextInput(
                attrs={'class': 'form-control tags', 'id': 'tags', 'placeholder': 'Etiket', 'required': 'required',
                       'rows': 3})

        }

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)

        if kwargs.get('instance'):
            print(kwargs.get('instance').categories.all())
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['categories'] = [t.pk for t in kwargs['instance'].categories.all()]
            self.fields['categories'].initial = initial['categories']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['categories'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%;', 'data-select2-id': '7',
                                                  'data-placeholder': 'Kategori Seçiniz'}
