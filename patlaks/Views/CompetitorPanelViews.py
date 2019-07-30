import json

import requests
import serializers
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


from patlaks.Forms.CompetitorNotificationForm import CompetitorNotificationForm
from patlaks.Forms.GetCompetitorForm import GetCompetitorForm
from patlaks.Forms.NotificationForm import NotificationForm
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


def send_notifications(request):
    notification_form = NotificationForm()
    competitor_filter = CompetitorNotificationForm()
    notifications = Notification.objects.all().order_by('id')

    if request.method == 'POST':
        notification_form = NotificationForm(request.POST)
        competitor_filter = CompetitorNotificationForm(request.POST)
        if notification_form.is_valid() and competitor_filter.is_valid():


            message = notification_form.cleaned_data['body']
            title = notification_form.cleaned_data['title']

            competitors = Competitor.objects.filter(birth_year__gte=competitor_filter.cleaned_data['startYear'],
                                                    birth_year__lte=competitor_filter.cleaned_data['endYear']).filter(
                gender__contains=competitor_filter.cleaned_data['gender'])

            headers = {
                "Authorization": "key=AAAAEgdR9KM:APA91bGJbWnT6MzzKIxRi9aAkfgyWCCRKxMNypBgpVjiM0ywTTU3xUyyK4_8Q3O8j-vVeY_k_genzinOnul2wDJKWQa3cnhuaHvG-3BVmdnjq3H1da1DHeKGjbF9ykimR-DlsC2ktnUw",
                "Content_Type": "application/json"}

            for competitor in competitors:
                payload = {
  "notification":
  {
    "title": title,
    "text": message,
    "sound": "default",
    "badge": "1",


  },
  "priority" : "high",
  "to": "fJoXrVnFMGE:APA91bEVu8K2xZDmS6GVXYL7-qp2eHCQs5pcr_gC2yYxB7tQhi7ModTz345GN8apaQoCts9NL6lX2V6SVaM6wg_Vx5c21IgrhSYMGea0umxzjh_JxaKatLYeNL0hgWXIBF6Ot_XApoY8",

}
                r = requests.post("https://fcm.googleapis.com/fcm/send", data=payload, headers=headers)

            notification = Notification(title=title, body=message,
                                        to=str(competitor_filter.cleaned_data['startYear']) + '-' +
                                           str(competitor_filter.cleaned_data['startYear']) + ' ' +
                                           competitor_filter.cleaned_data['gender'], is_send=True)

            notification.save()

        # payload = {"registration_ids":
        #   [
        #      "fJoXrVnFMGE:APA91bEVu8K2xZDmS6GVXYL7-qp2eHCQs5pcr_gC2yYxB7tQhi7ModTz345GN8apaQoCts9NL6lX2V6SVaM6wg_Vx5c21IgrhSYMGea0umxzjh_JxaKatLYeNL0hgWXIBF6Ot_XApoY8"],
        # "data": {"title": "aaaas", "alert": "Babanın düşmanlarını yiyim."}}

        # r = requests.post("https://fcm.googleapis.com/fcm/send", data=payload, headers=headers)

    return render(request, 'send-notification.html',
                  {'notifications': notifications, 'form_notification': notification_form,
                   'filter_form': competitor_filter})
