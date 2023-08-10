from django.urls import path
from .views import create_landlord, landlord_info


urlpatterns = [
    path('signup/', create_landlord, name='create_landlord'),
    path("", landlord_info, name='landlord_info'),
]
