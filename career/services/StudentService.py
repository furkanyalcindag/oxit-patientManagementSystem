import traceback

from django.contrib.auth.models import Group, User

from career.models import Student
from career.models.MilitaryStatus import MilitaryStatus
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


def add_military_status(uuid, military_status_id):
    student = Student.objects.get(uuid=uuid)
    military_status = MilitaryStatus.objects.get(id=military_status_id)
    student.profile.militaryStatus = military_status
    student.save()


def get_military_status(uuid):
    student = Student.objects.get(uuid=uuid)

