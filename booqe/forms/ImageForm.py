from django.forms import ModelForm

from booqe.models import BlogImage


class ImageForm(ModelForm):
    class Meta:
        model = BlogImage
        fields = ('blogImage',)
