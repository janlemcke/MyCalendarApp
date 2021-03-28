from django.urls import path
from mycalendar.views import homeView


urlpatterns = [
    path('home', homeView, name="home"),
]