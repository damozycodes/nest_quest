from django.urls import path

from . import views


app_name = "listings"
urlpatterns = [
	path("new/", views.NewListingView.as_view(), name="new"),
	path("<uuid:pk>/", views.ListingView.as_view(), name= "listing"),
    path("by/<uuid:pk>/", views.ListListingView.as_view(), name= "by"),
    path("search/", views.SearchListingView.as_view(), name= "search"),
    path("<uuid:pk>/like/", views.LikeListingView.as_view(), name= "like"),
    path("likes/mine/", views.MyLikedListingsView.as_view(), name= "likes"),
]