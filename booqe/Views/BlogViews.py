from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from booqe.forms.BlogForm import BlogForm
from booqe.forms.ImageForm import ImageForm
from booqe.models import Profile, BlogImage, Blog


def add_blog(request):
    blogs = Blog.objects.all()
    blog_form = BlogForm()
    ImageFormSet = modelformset_factory(BlogImage,
                                        form=ImageForm, extra=4)
    formset = ImageFormSet(queryset=BlogImage.objects.none())

    if request.method == 'POST':

        blog_form = BlogForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=BlogImage.objects.none())
        blog = blog_form.save(commit=False)
        blog.blogOwner = Profile.objects.get(user=request.user)
        blog.save()

        for category in blog_form.cleaned_data['categories']:
            blog.categories.add(category)

        blog.save()

        for form in formset.cleaned_data:
            # this helps to not crash if the user
            # do not upload all the photos
            if form:
                image = form['blogImage']
                photo = BlogImage(blog=blog, blogImage=image)
                photo.save()
        messages.success(request, "Blog eklendi")

        return redirect('booqe:add-blog')

    return render(request, 'blog-share.html', {'blog_form': blog_form, 'formset': formset, 'blogs': blogs})


def return_blog_images(request, pk):
    blog_images = BlogImage.objects.filter(blog_id=pk)
    return render(request, 'blog-images.html', {'blog_images': blog_images})
