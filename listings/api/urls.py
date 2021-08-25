from django.urls import path
from .views import *


urlpatterns = [

    path("",
    GetAvailableRoomsAPIView.as_view(),
             name="booking-list"),

]