from django.contrib.auth.models import User
from django.shortcuts import render

from booqe.models.PinnedBlog import PinnedBlog


def dashboard(request):
    users_count = User.objects.count()
    pinned_count = PinnedBlog.objects.count()

    return render(request, 'dashboard-temp.html', {'user_count': users_count,'pinned_count':pinned_count})