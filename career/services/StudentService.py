import traceback

from django.contrib.auth.models import Group, User

from career.models.Profile import Profile


def add_student(first_name, last_name, mail, password):
    try:
        group = Group.objects.get(name__exact="Student")
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.username = mail
        user.email = mail
        user.groups.add(group)
        user.save()
        profile = Profile()
        profile.user = user
        profile.save()
        return user
    except Exception:
        traceback.print_exc()
        raise ValueError("Unique email")









