from rest_framework import serializers

from booqe.models import Blog, Category, Profile
from booqe.models.PinnedBlog import PinnedBlog
from booqe.serializers.UserSerializer import ProfileSerializerFlutter


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        depth = 2


class ImageSourceSerializer(serializers.Serializer):
    imageSource = serializers.ImageField()


class ImageSource2Serializer(serializers.Serializer):
    imageSource = serializers.CharField()


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ProfileSerializer(serializers.Serializer):
    photo = ImageSourceSerializer()
    about = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    gender = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.IntegerField()
    height = serializers.IntegerField()
    inseam = serializers.IntegerField()
    email = serializers.CharField()
    phoneNumber = serializers.CharField()
    friends = RecursiveField(many=True)
    onLine = serializers.BooleanField()


class BlogAppSerializer(serializers.Serializer):
    # user = serializers.HyperlinkedIdentityField(view_name='patlaks:user-detail', lookup_field='pk')
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    content = serializers.CharField()
    image = ImageSourceSerializer()
    author = ProfileSerializer()
    date = serializers.CharField()
    tips = serializers.CharField()
    comments = serializers.CharField()
    likes = serializers.CharField()


class BlogAppSerializerFlutter(serializers.Serializer):
    # user = serializers.HyperlinkedIdentityField(view_name='patlaks:user-detail', lookup_field='pk')
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    content = serializers.CharField()
    image = serializers.ImageField()
    pin = serializers.BooleanField()


class CategoryAppSerializer(serializers.Serializer):
    # user = serializers.HyperlinkedIdentityField(view_name='patlaks:user-detail', lookup_field='pk')
    id = serializers.IntegerField()
    title = serializers.CharField()
    icon = ImageSourceSerializer()
    route = serializers.CharField()


class CategoryAppSerializerFlutter(serializers.Serializer):
    # user = serializers.HyperlinkedIdentityField(view_name='patlaks:user-detail', lookup_field='pk')
    id = serializers.IntegerField()
    categoryName = serializers.CharField()
    categoryImage = serializers.ImageField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 2


class PinBlogSerializer(serializers.Serializer):
    blog_id = serializers.IntegerField(required=True, write_only=True)

    def create(self, validated_data):

        profile = Profile.objects.get(user=self.context['request'].user)

        pinned_blog = PinnedBlog.objects.filter(blog_id=validated_data.get('blog_id'),
                                                profile=profile)

        pinned = False

        if pinned_blog.count() > 0:
            pinned_blog[0].delete()
            pinned = False

        else:
            pinned_blog = PinnedBlog()
            pinned_blog.blog_id = validated_data['blog_id']
            pinned_blog.profile = profile
            pinned_blog.save()
            pinned = True

        return pinned


class CekilisSerializer(serializers.Serializer):
    users = ProfileSerializerFlutter(many=True)
    blog = serializers.CharField()
    title = serializers.CharField()
    pinned_count = serializers.IntegerField()
    blog_image = serializers.ImageField()
