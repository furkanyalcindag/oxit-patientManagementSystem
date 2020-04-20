from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from booqe.forms.BlogForm import BlogForm
from booqe.forms.ImageForm import ImageForm
from booqe.models import Profile, BlogImage, Blog


def add_blog(request):
    blogs = Blog.objects.all().order_by('-id')
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


@user_passes_test(lambda u: u.is_superuser)
def blogs(request):
    blogs = Blog.objects.all().order_by('-id')
    return render(request, 'blogs.html', {'blogs': blogs})


def return_blog_images(request, pk):
    blog_images = BlogImage.objects.filter(blog_id=pk)
    return render(request, 'blog-images.html', {'blog_images': blog_images})


def update_blog(request, pk):
    blogs = Blog.objects.all()
    blog = Blog.objects.get(pk=pk)
    blog_form = BlogForm(request.POST or None, instance=blog)
    ImageFormSet = modelformset_factory(BlogImage,
                                        form=ImageForm, extra=4)
    formset = ImageFormSet(queryset=BlogImage.objects.none())

    if request.method == 'POST':

        # blog_form = BlogForm(request.POST)
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


def delete_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    blogImage = BlogImage.objects.filter(blog=blog)
    blogImage.delete()

    blog.delete()
    return redirect('booqe:add-blog')


def delete_image(request, pk):
    blogImage = BlogImage.objects.get(pk=pk)
    blog_id = blogImage.blog.id
    blogImage.delete()

    return redirect('booqe:blog-images', blog_id)
