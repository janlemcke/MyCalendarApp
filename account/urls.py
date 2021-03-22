from django.urls import path, include
from account.views import loginView

urlpatterns = [
    path('', loginView, name="login")
]