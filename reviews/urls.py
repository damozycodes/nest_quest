from django.urls import path

from . import views


app_name = "reviews"
urlpatterns = [
    path("new/<uuid:pk>/", views.NewReviewView.as_view(), name="new"),
    path("<int:pk>/", views.ReviewView.as_view(), name= "review"),
    path("listing/<uuid:pk>/", views.ListingReviewView.as_view(), name= "listing"),
    path("mine/", views.UserReviewView.as_view(), name= "user"),
]