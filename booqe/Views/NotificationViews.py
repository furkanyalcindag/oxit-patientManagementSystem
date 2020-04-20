import json

import requests
from django.contrib import messages
from django.shortcuts import redirect, render

from booqe.forms.NotificationForm import NotificationForm
from booqe.models import Profile, Notification


def send_notify(request):
    notification_form = NotificationForm()
    notifications = Notification.objects.all().order_by('-id')

    if request.method == 'POST':
        notification_form = NotificationForm(request.POST)
        if notification_form.is_valid():
            message = notification_form.cleaned_data['body']
            title = notification_form.cleaned_data['title']
            success = 0
            failure = 0

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=AAAA8oGE4Pk:APA91bHILgxtLUJbgTXuuaKTStnuUXcYjfTSb4I9HSYiCsSKmMe1rfeIzdtp61a8soGtLGlLBEG1td18ztWuS5lYkaciDoGdmpxHS1DJe5NaKrV_qaHymKnpFZYTfIFOvfanazfyPnBv',
            }

            tokens = []

            profiles = Profile.objects.filter(notification=True)

            for profile in profiles:
                data = '{"notification": {"body": "' + message + '","title": "' + title + '"}, "priority": "high", "data": {"click_action": "FLUTTER_NOTIFICATION_CLICK", "id": "1", "status": "done"}, "to": "' + profile.gcm_registerID + '"}'

                response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=data.encode('utf-8'))
                a = response
                if json.loads(a.text)['success'] == 0:
                    failure = failure + 1
                else:
                    success = success + 1

            notification = Notification(title=title, body=message,
                                        to='Herkes, Başarılı:' + str(success) + ' Başarısız:' + str(failure),
                                        is_send=True)
            notification.save()

            messages.success(request, "Başarıyla Gönderildi")

            return redirect('booqe:send')

    return render(request, 'send-google-notification.html',
                  {'form_notification': notification_form, 'notifications': notifications})
