from django.conf.urls import url

from booqe.Views import BlogViews, BlogApiViews, UserAPIViews

app_name = 'booqe'

urlpatterns = [

    url(r'blog/$', BlogViews.add_blog, name='add-blog'),
    url(r'blog-images/(?P<pk>\d+)$', BlogViews.return_blog_images, name='blog-images'),

    # api
    url(r'blogs-api-get/$', BlogApiViews.GetBlogsLatest.as_view(), name='api-get'),
    url(r'blogs-api-get-by-cat/$', BlogApiViews.GetBlogsByCategory.as_view(), name='api-get-by-category'),
    url(r'blog-api-get-by-id/$', BlogApiViews.GetBlogById.as_view(), name='api-get-blog-by-id'),
    url(r'categories-api-get/$', BlogApiViews.GetCategories.as_view(), name='api-get-categories'),
    url(r'blogs-api-get-by-pin/$', BlogApiViews.GetBlogsByPin.as_view(), name='api-get-blog-by-pin'),

    url(r'blogs-api-pin/$', BlogApiViews.DoPinBlog.as_view(), name='api-do-pin'),

    # user-api
    url(r'register-api/$', UserAPIViews.CreateUserMember.as_view(), name='register-api'),
    url(r'profile-info-api/$', UserAPIViews.ProfileInformation.as_view(), name='profile-info-api'),
    url(r'profile-notification-api/$', UserAPIViews.NotificationApi.as_view(), name='notification-api'),
    url(r'change-password/$', UserAPIViews.ChangePassword.as_view(), name='change-password-api'),
    url(r'change-profile-image/$', UserAPIViews.ChangeProfileImage.as_view(), name='change-profile-image-api'),
]
