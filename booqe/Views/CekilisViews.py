from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from booqe.models import Blog
from booqe.models.CekilisObject import CekilisObject
from booqe.models.PinnedBlog import PinnedBlog
from booqe.models.ProfileObject import ProfileObjectForFlutter
from booqe.serializers.BlogSerializer import CekilisSerializer


def cekilis_ekran(request):
    blogs = Blog.objects.filter(isPublish=True)

    return render(request, 'cekilis-ekran.html', {'blogs': blogs})


@api_view(http_method_names=['POST'])
def prepare_cekilis(request):

        try:

            blog_id =int(request.POST.get('blog_id'))
            #blog_id =request.data['blog_id']
            users = []
            blog = Blog.objects.get(pk=blog_id)
            pinned_blogs = PinnedBlog.objects.filter(blog=blog)

            for pin in pinned_blogs:
                user = ProfileObjectForFlutter(profileImage=pin.profile.profileImage,
                                               username=pin.profile.user.username, pinCount=0)
                users.append(user)

            cekilis_object = CekilisObject()
            cekilis_object.blog = blog.description
            cekilis_object.title = blog.title
            cekilis_object.pinned_count = pinned_blogs.count()
            cekilis_object.users = users
            cekilis_object.blog_image = blog.blogimage_set.all()[0].blogImage

            data = CekilisSerializer(cekilis_object)
            responseData = dict()
            responseData['cekilis_hazirla'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})

