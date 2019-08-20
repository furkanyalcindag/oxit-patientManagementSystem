import json
import calendar
from datetime import datetime
import datetime

import requests
import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Max, Min
from django.http import JsonResponse, request
from django.shortcuts import render, redirect

from patlaks.Forms.CompetitorNotificationForm import CompetitorNotificationForm
from patlaks.Forms.GetCompetitorForm import GetCompetitorForm
from patlaks.Forms.MessageForm import MessageForm
from patlaks.Forms.NotificationForm import NotificationForm
from patlaks.models import Score
from patlaks.models.Message import Message
from patlaks.models.Menu import Menu
from patlaks.models.Competitor import Competitor
from patlaks.models.Notification import Notification


@login_required
def get_competitors(request):
    form = GetCompetitorForm()
    competitors = Competitor.objects.all().order_by('-id')[:100]
    competitor_count = Competitor.objects.all().count()

    if request.method == 'POST':
        form = GetCompetitorForm(request.POST)
        return render(request, 'get-competitor.html', {'competitors': competitors})

    competitors = Competitor.objects.all().order_by('-id')
    return render(request, 'get-competitor.html',
                  {'competitors': competitors, 'count': competitor_count, 'show_record': competitors.count(),
                   'form': form})


@login_required
def send_notifications(request):
    notification_form = NotificationForm()
    competitor_filter = CompetitorNotificationForm()
    notifications = Notification.objects.all().order_by('-id')

    if request.method == 'POST':
        notification_form = NotificationForm(request.POST)
        competitor_filter = CompetitorNotificationForm(request.POST)
        if notification_form.is_valid() and competitor_filter.is_valid():

            message = notification_form.cleaned_data['body']
            title = notification_form.cleaned_data['title']
            success = 0
            failure = 0

            competitors = Competitor.objects.filter(birth_year__gte=competitor_filter.cleaned_data['startYear'],
                                                    birth_year__lte=competitor_filter.cleaned_data['endYear']).filter(
                gender__contains=competitor_filter.cleaned_data['gender'])

            headers = {
                'Authorization': 'key=AAAAEgdR9KM:APA91bGJbWnT6MzzKIxRi9aAkfgyWCCRKxMNypBgpVjiM0ywTTU3xUyyK4_8Q3O8j-vVeY_k_genzinOnul2wDJKWQa3cnhuaHvG-3BVmdnjq3H1da1DHeKGjbF9ykimR-DlsC2ktnUw',
                'Content-Type': 'application/json'}

            for competitor in competitors:
                payload = {"to":

                               competitor.gcm_registerID,
                           "data": {"title": title, "alert": message}
                           }

                if competitor.notification:

                    r = requests.post("https://fcm.googleapis.com/fcm/send", data=json.dumps(payload), headers=headers)

                    if json.loads(r.text)['success'] == 0:
                        failure = failure + 1
                    else:
                        success = success + 1
                else:
                    failure = failure+1

            notification = Notification(title=title, body=message,
                                        to=str(competitor_filter.cleaned_data['startYear']) + '-' +
                                           str(competitor_filter.cleaned_data['endYear']) + ' ' +
                                           competitor_filter.cleaned_data[
                                               'gender'] + ' ' + 'Başarılı:' + str(success) + ' Başarısız' + str(
                                            failure),
                                        is_send=True)

            notification.save()

            messages.success(request, "Başarıyla Kaydedildi")

            return redirect('patlaks:send-notification')

        # payload = {"registration_ids":
        #   [
        #      "fJoXrVnFMGE:APA91bEVu8K2xZDmS6GVXYL7-qp2eHCQs5pcr_gC2yYxB7tQhi7ModTz345GN8apaQoCts9NL6lX2V6SVaM6wg_Vx5c21IgrhSYMGea0umxzjh_JxaKatLYeNL0hgWXIBF6Ot_XApoY8"],
        # "data": {"title": "aaaas", "alert": "Babanın düşmanlarını yiyim."}}

        # r = requests.post("https://fcm.googleapis.com/fcm/send", data=payload, headers=headers)

    return render(request, 'send-notification.html',
                  {'notifications': notifications, 'form_notification': notification_form,
                   'filter_form': competitor_filter})


@login_required
def send_message(request):
    message_form = MessageForm()

    messages1 = Message.objects.all().order_by('-id')

    if request.method == 'POST':
        message_form = MessageForm(request.POST)

        if message_form.is_valid():

            message = message_form.cleaned_data['body']
            who = message_form.cleaned_data['to']
            success = 0
            failure = 0

            try:

                user = User.objects.get(username=who)

                competitors = Competitor.objects.filter(user=user)

                headers = {
                    'Authorization': 'key=AAAAEgdR9KM:APA91bGJbWnT6MzzKIxRi9aAkfgyWCCRKxMNypBgpVjiM0ywTTU3xUyyK4_8Q3O8j-vVeY_k_genzinOnul2wDJKWQa3cnhuaHvG-3BVmdnjq3H1da1DHeKGjbF9ykimR-DlsC2ktnUw',
                    'Content-Type': 'application/json'}

                for competitor in competitors:
                    payload = {"to":

                                   competitor.gcm_registerID,
                               "data": {"title": "mesaj", "alert": message}
                               }
                    r = requests.post("https://fcm.googleapis.com/fcm/send", data=json.dumps(payload), headers=headers)

                    if json.loads(r.text)['success'] == 0:
                        message = Message(body=message,
                                          to=competitor,
                                          is_send=False)
                        message.save()

                        messages.success(request, "Mesaj Gönderilemedi")
                    else:
                        message = Message(body=message,
                                          to=competitor,
                                          is_send=True)
                        message.save()

                        messages.success(request, "Mesaj Gönderildi")

            except Exception as e:
                messages.success(request, "Mesaj Gönderilemedi")

            return redirect('patlaks:send-message')

        # payload = {"registration_ids":
        #   [
        #      "fJoXrVnFMGE:APA91bEVu8K2xZDmS6GVXYL7-qp2eHCQs5pcr_gC2yYxB7tQhi7ModTz345GN8apaQoCts9NL6lX2V6SVaM6wg_Vx5c21IgrhSYMGea0umxzjh_JxaKatLYeNL0hgWXIBF6Ot_XApoY8"],
        # "data": {"title": "aaaas", "alert": "Babanın düşmanlarını yiyim."}}

        # r = requests.post("https://fcm.googleapis.com/fcm/send", data=payload, headers=headers)

    return render(request, 'send-message.html',
                  {'messages': messages1, 'form_message': message_form})


@login_required
def get100(request):
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]

    scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).values(
        'competitor').annotate(score=Min('score')).order_by('score')[:100]

    my_objects = []

    for score in scores:
        new = Competitor.objects.get(id=score['competitor'])
        newScore = Score()
        newScore.competitor = new
        newScore.score = score['score']
        my_objects.append(newScore)

    return render(request, 'get-top-100.html', {'scores': my_objects})


@login_required
def get_username(request):
    if request.POST:
        try:
            username = request.POST.get('term')

            users = User.objects.filter(username=username)

            return JsonResponse(json.dumps(users))

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def dashboard(request):
    total_user = Competitor.objects.all().count()
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    active_user_weekly = User.objects.filter(last_login__range=(last_week, today)).count()
    newuser_montly = User.objects.filter(date_joined__month=today.month).count()

    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).values(
        'competitor').annotate(score=Min('score')).order_by('score')[:100]

    my_objects = []

    for score in scores:
        new = Competitor.objects.get(id=score['competitor'])
        newScore = Score()
        newScore.competitor = new
        newScore.score = score['score']
        my_objects.append(newScore)

    return render(request, 'dashboard.html',
                  {'total_user': total_user, 'active_user_weekly': active_user_weekly,
                   'new_user_monthly': newuser_montly, 'top10': my_objects})


@login_required
def menu(request):
    anasayfa = Menu(name="Anasayfa", url="", is_parent=True, is_show=True,
                    fa_icon='fa-home')

    anasayfa.save()

    menuDashboard = Menu(name="İstatistikler", url="patlaks:dashboard", is_parent=False, is_show=True, parent=anasayfa,
                         fa_icon='fa-calculator')
    menuDashboard = menuDashboard.save()

    menuUsers = Menu(name="Kullanıcılar", url="", is_parent=True, is_show=True,
                     fa_icon='fa-user')
    menuUsers = menuUsers.save()

    submenucompetitor = Menu(name="Yarışmacılar", url="patlaks:competitor-list", is_parent=False, parent=menuUsers,
                             is_show=True,
                             fa_icon='fa-user')

    submenucompetitor.save()

    submenucompetitorwins = Menu(name="Top 100 Listesi", url="patlaks:get-top", is_parent=False, parent=menuUsers,
                                 is_show=True,
                                 fa_icon='fa-signal')

    submenucompetitorwins.save()

    menuMessage = Menu(name="Mesaj İşlemleri", url="", is_parent=True, is_show=True,
                       fa_icon='fa-envelope-o')

    menuMessage.save()
    submenuSendNotification = Menu(name="Bildirim Gönder", url="patlaks:send-notification", is_parent=False,
                                   parent=menuMessage,
                                   is_show=True,
                                   fa_icon='fa-commenting')

    submenuSendNotification.save()

    submenuSendMessage = Menu(name="Mesaj Gönder", url="patlaks:send-message", is_parent=False,
                              parent=menuMessage,
                              is_show=True,
                              fa_icon=' fa-sticky-note-o')

    submenuSendMessage.save()

    menuAddmob = Menu(name="Reklam", url="", is_parent=True, is_show=True,
                      fa_icon='fa-amazon')

    menuAddmob.save()

    return JsonResponse({"success": "OK"})


