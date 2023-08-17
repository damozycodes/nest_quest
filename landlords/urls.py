from django.urls import path
from . import views

app_name = "landlord"
urlpatterns = [
    path('signup/', views.CreateLandlordView.as_view(), name='signup'),
    path("", views.LandlordInfoView.as_view(), name='landlord'),
]
