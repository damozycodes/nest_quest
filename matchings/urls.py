from django.urls import path

from . import views


app_name = "matchings"
urlpatterns = [
    path("new/", views.NewMatchingRequestView.as_view(), name="new"),
    path("mine/", views.MatchingRequestView.as_view(), name="mine"),
    path("get/", views.GetMatchingsView.as_view(), name="similar"),
]