from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from booqe.models import Profile, Blog, Category, BlogImage, CategoryImage
from booqe.models.BlogObject import BlogObject
from booqe.models.CategoryObject import CategoryObject
from booqe.models.CategoryObject2 import CategoryObject2
from booqe.models.ImageSourceObject import ImageSourceObject
from booqe.models.PinnedBlog import PinnedBlog
from booqe.models.ProfileObject import ProfileObject
from booqe.serializers.BlogSerializer import BlogSerializer, CategorySerializer, BlogAppSerializer, \
    ImageSourceSerializer, CategoryAppSerializer, CategoryAppSerializerFlutter, BlogAppSerializerFlutter, \
    PinBlogSerializer


class GetBlog(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        # user_pk = request.user.id

        # user_request = User.objects.get(pk=user_pk)
        # competitor_request = Profile.objects.get(user=user_request)
        blogs = Blog.objects.all()
        blog_api = []

        for blog in blogs:
            if BlogImage.objects.filter(blog=blog).count() > 0:
                image = BlogImage.objects.filter(blog=blog)[0].blogImage
            else:
                image = None

            ImageSource = ImageSourceObject(imageSource=image)
            # serializerImage = ImageSourceSerializer(imageSource)

            # imageSource = ImageSourceObject(imageSource=imageSource)

            ImageSource2 = ImageSourceObject(imageSource=Profile.objects.get(user__username='admin').profileImage)
            author_object = ProfileObject(photo=ImageSource2, about="jhsjkhdkjs", firstName="Aybukenur",
                                          lastName="Demirci",
                                          gender="Erkek", age=27, weight=180, height=180, inseam=21,
                                          email="jhssds@sdns.com", phoneNumber="asasa", location="Türkiye",
                                          friends=None, onLine=True)

            blog_object = BlogObject(title=blog.title,
                                     description='deneme blogdeneme blogdeneme blogdeneme blogdeneme blogdeneme blogdeneme blogdeneme blog',
                                     content=blog.blog, comments=None,
                                     image=ImageSource,
                                     likes=1250, author=author_object, date=None, tips=None)
            blog_api.append(blog_object)

        serializer_context = {
            'request': request,
        }
        # serializer = BlogSerializer(blogs, many=True, context=serializer_context)
        serializer = BlogAppSerializer(blog_api, many=True, context=serializer_context)
        return Response(serializer.data)


class GetCategories(APIView):
    permission_classes = (IsAuthenticated,)
    '''def get(self, request, format=None):
        array_category = []

        categories = Category.objects.all()
        for category in categories:
            x = BlogImage.objects.filter(pk=1)[0].blogImage
            ImageSource = ImageSourceObject(imageSource=CategoryImage.objects.get(category=category).categoryImage)
            icon = ImageSource
            categoryObject = CategoryObject(id=category.pk, title=category.categoryName, icon=icon,
                                            route='Article List 2')
            array_category.append(categoryObject)

        serializer_context = {
            'request': request,
        }
        serializer = CategoryAppSerializer(array_category, many=True, context=serializer_context)
        return Response(serializer.data)'''

    def get(self, request, format=None):
        array_category = []

        categories = Category.objects.all()
        for category in categories:
            x = BlogImage.objects.filter(pk=1)[0].blogImage
            ImageSource = ImageSourceObject(imageSource=CategoryImage.objects.get(category=category).categoryImage)
            icon = ImageSource
            categoryObject = CategoryObject2(id=category.pk, categoryName=category.categoryName,
                                             categoryImage=CategoryImage.objects.get(category=category).categoryImage)
            array_category.append(categoryObject)

        serializer_context = {
            'request': request,
        }
        serializer = CategoryAppSerializerFlutter(array_category, many=True, context=serializer_context)
        return Response(serializer.data)


class GetBlogsByCategory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        array_category = []

        category = Category.objects.get(pk=request.query_params['catId'])

        blog_api = []

        user = request.user

        profile = Profile.objects.get(user=user)

        for blog in category.blog_set.all():
            if BlogImage.objects.filter(blog=blog).count() > 0:
                image = BlogImage.objects.filter(blog=blog)[0].blogImage
            else:
                image = None

            ImageSource = ImageSourceObject(imageSource=image)
            # serializerImage = ImageSourceSerializer(imageSource)

            # imageSource = ImageSourceObject(imageSource=imageSource)

            # ImageSource2 = ImageSourceObject(imageSource=Profile.objects.get(user__username='admin').profileImage)
            """author_object = ProfileObject(photo=ImageSource2, about="jhsjkhdkjs", firstName="Aybukenur",
                                          lastName="Demirci",
                                          gender="Erkek", age=27, weight=180, height=180, inseam=21,
                                          email="jhssds@sdns.com", phoneNumber="asasa", location="Türkiye",
                                          friends=None, onLine=True)"""
            pinned = PinnedBlog.objects.filter(blog=blog, profile=profile)

            if pinned.count() > 0:
                blog_object = BlogObject(id=blog.id, title=blog.title,
                                         description=blog.description,
                                         content=blog.blog, date=blog.creationDate,
                                         image=image, pin=True
                                         )
            else:
                blog_object = BlogObject(id=blog.id, title=blog.title,
                                         description=blog.description,
                                         content=blog.blog, date=blog.creationDate,
                                         image=image, pin=False
                                         )

            blog_api.append(blog_object)

        serializer_context = {
            'request': request,
        }
        # serializer = BlogSerializer(blogs, many=True, context=serializer_context)
        serializer = BlogAppSerializerFlutter(blog_api, many=True, context=serializer_context)
        return Response(serializer.data)


class GetBlogsByPin(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        array_category = []

        user = request.user

        profile = Profile.objects.get(user=user)

        blogs = PinnedBlog.objects.filter(profile=profile).order_by('-id')

        blog_api = []

        for blog in blogs:
            if BlogImage.objects.filter(blog=blog.blog).count() > 0:
                image = BlogImage.objects.filter(blog=blog.blog)[0].blogImage
            else:
                image = None

            ImageSource = ImageSourceObject(imageSource=image)
            # serializerImage = ImageSourceSerializer(imageSource)

            # imageSource = ImageSourceObject(imageSource=imageSource)

            # ImageSource2 = ImageSourceObject(imageSource=Profile.objects.get(user__username='admin').profileImage)
            """author_object = ProfileObject(photo=ImageSource2, about="jhsjkhdkjs", firstName="Aybukenur",
                                          lastName="Demirci",
                                          gender="Erkek", age=27, weight=180, height=180, inseam=21,
                                          email="jhssds@sdns.com", phoneNumber="asasa", location="Türkiye",
                                          friends=None, onLine=True)"""

            blog_object = BlogObject(id=blog.blog.id, title=blog.blog.title,
                                     description=blog.blog.description,
                                     content=blog.blog.blog, date=blog.blog.creationDate,
                                     image=image, pin=True
                                     )
            blog_api.append(blog_object)

        serializer_context = {
            'request': request,
        }
        # serializer = BlogSerializer(blogs, many=True, context=serializer_context)
        serializer = BlogAppSerializerFlutter(blog_api, many=True, context=serializer_context)
        return Response(serializer.data)


class GetBlogById(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        array_category = []
        user = request.user

        profile = Profile.objects.get(user=user)
        blog = Blog.objects.get(pk=int(request.query_params['blogId']))

        if BlogImage.objects.filter(blog=blog).count() > 0:
            image = BlogImage.objects.filter(blog=blog)[0].blogImage
        else:
            image = None

        image = BlogImage.objects.filter(blog=blog)[0].blogImage

        ImageSource = ImageSourceObject(imageSource=image)
        # serializerImage = ImageSourceSerializer(imageSource)

        # imageSource = ImageSourceObject(imageSource=imageSource)

       # ImageSource2 = ImageSourceObject(imageSource=Profile.objects.get(user__username='admin').profileImage)
        '''author_object = ProfileObject(photo=ImageSource2, about="jhsjkhdkjs", firstName="Aybukenur",
                                      lastName="Demirci",
                                      gender="Erkek", age=27, weight=180, height=180, inseam=21,
                                      email="jhssds@sdns.com", phoneNumber="asasa", location="Türkiye",
                                      friends=None, onLine=True)'''

        pinned = PinnedBlog.objects.filter(blog=blog, profile=profile)

        if pinned.count() > 0:
            blog_object = BlogObject(id=blog.id, title=blog.title,
                                     description=blog.description,
                                     content=blog.blog, date=blog.creationDate,
                                     image=image, pin=True
                                     )
        else:
            blog_object = BlogObject(id=blog.id, title=blog.title,
                                     description=blog.description,
                                     content=blog.blog, date=blog.creationDate,
                                     image=image, pin=False
                                     )

        array_category.append(blog_object)



        blog_api = []

        serializer_context = {
            'request': request,
        }
        # serializer = BlogSerializer(blogs, many=True, context=serializer_context)
        serializer = BlogAppSerializerFlutter(array_category,many=True, context=serializer_context)

        return Response(serializer.data)


class DoPinBlog(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        return Response({"message": "pinned"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PinBlogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "pinned"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GetBlogsLatest(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        array_category = []

        blog_api = []

        user = request.user

        profile = Profile.objects.get(user=user)

        blogs = Blog.objects.filter().order_by('-id')[:20]

        for blog in blogs:
            if BlogImage.objects.filter(blog=blog).count() > 0:
                image = BlogImage.objects.filter(blog=blog)[0].blogImage
            else:
                image = None

            ImageSource = ImageSourceObject(imageSource=image)
            # serializerImage = ImageSourceSerializer(imageSource)

            # imageSource = ImageSourceObject(imageSource=imageSource)

            # ImageSource2 = ImageSourceObject(imageSource=Profile.objects.get(user__username='admin').profileImage)
            """author_object = ProfileObject(photo=ImageSource2, about="jhsjkhdkjs", firstName="Aybukenur",
                                          lastName="Demirci",
                                          gender="Erkek", age=27, weight=180, height=180, inseam=21,
                                          email="jhssds@sdns.com", phoneNumber="asasa", location="Türkiye",
                                          friends=None, onLine=True)"""
            pinned = PinnedBlog.objects.filter(blog=blog, profile=profile)

            if pinned.count() > 0:
                blog_object = BlogObject(id=blog.id, title=blog.title,
                                         description=blog.description,
                                         content=blog.blog, date=blog.creationDate,
                                         image=image, pin=True
                                         )
            else:
                blog_object = BlogObject(id=blog.id, title=blog.title,
                                         description=blog.description,
                                         content=blog.blog, date=blog.creationDate,
                                         image=image, pin=False
                                         )

            blog_api.append(blog_object)

        serializer_context = {
            'request': request,
        }
        # serializer = BlogSerializer(blogs, many=True, context=serializer_context)
        serializer = BlogAppSerializerFlutter(blog_api, many=True, context=serializer_context)
        return Response(serializer.data)
