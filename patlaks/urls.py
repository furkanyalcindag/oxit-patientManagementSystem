from django.conf.urls import url, include
from django.urls import path

from patlaks.Views import CompetitorViews, CompetitorApiViews2, CompetitorPanelViews

app_name = 'patlaks'

urlpatterns = [
    url(r"articles$", CompetitorViews.CompetitorList.as_view(),
        name="api-article-list"),
    # url(r'fake/$', FakeViews.generateFake, name='fake'),

    url(r'competitor-list/$', CompetitorApiViews2.competitor_list, name='deneme-ssdsdsd'),

    url(r'add-reference/$', CompetitorViews.AddReference.as_view(), name="add-reference"),

    url(r'change-password/$', CompetitorViews.ChangePassword.as_view(), name="change-password"),

    url(r'update-competitor/$', CompetitorViews.UpdateCompetitor.as_view(), name="update-competitor"),

    url(r'add-score/$', CompetitorViews.AddScore.as_view(), name='add-score'),



    url(r'get-self-10-score/$', CompetitorViews.GetCompetitorScore.as_view(), name='get-self-10-score'),

    url(r'get-100-score/$', CompetitorViews.GetTop100.as_view(), name='get-100-score'),

    url(r'get-references/$', CompetitorViews.GetChildrenCompetitors.as_view(), name='get-references'),

    url(r'get-messages/$', CompetitorViews.GetCompetitorMessage.as_view(), name='get-message'),

    url(r'get-competitor/$', CompetitorViews.CompetitorGet.as_view(), name='get-competitor'),

    url(r'notification-settings/$', CompetitorViews.NotificationGet.as_view(), name='notification-settings'),
    url(r'bank-info/$', CompetitorViews.UpdateBank.as_view(), name='update-bank'),

    # Panel Bilgileri

    url(r'competitor/$', CompetitorPanelViews.get_competitors, name='competitor-list'),

    url(r'send-notifications/$', CompetitorPanelViews.send_notifications, name='send-notification'),

    url(r'get-top-100/$', CompetitorPanelViews.get100, name='get-top'),





    url(r'send-message/$', CompetitorPanelViews.send_message, name='send-message'),

    url(r'add-menu/$', CompetitorPanelViews.menu, name='add-menu'),

    url('', CompetitorPanelViews.dashboard, name='dashboard'),



]
