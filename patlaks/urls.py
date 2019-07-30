from django.conf.urls import url, include
from django.urls import path

from patlaks.Views import CompetitorViews, CompetitorApiViews2, CompetitorPanelViews


app_name = 'patlaks'

urlpatterns = [
    url(r"articles$", CompetitorViews.CompetitorList.as_view(),
        name="api-article-list"),
    #url(r'fake/$', FakeViews.generateFake, name='fake'),

    url(r'competitor-list/$', CompetitorApiViews2.competitor_list, name='deneme-ssdsdsd'),



    url(r'add-reference/$', CompetitorViews.AddReference.as_view(), name="add-reference"),

    url(r'add-score/$',CompetitorViews.AddScore.as_view(), name='add-score'),

    url(r'get-self-10-score/$',CompetitorViews.GetCompetitorScore.as_view(), name='get-self-10-score'),

    url(r'get-100-score/$',CompetitorViews.GetTop100.as_view(), name='get-100-score'),

    url(r'get-references/$', CompetitorViews.GetChildrenCompetitors.as_view(), name='get-100-score'),



    #Panel Bilgileri

    url(r'yarismacilar/$', CompetitorPanelViews.get_competitors, name='competitor-list'),

    url(r'send-notifications/$', CompetitorPanelViews.send_notifications, name='send-notification'),


    ]