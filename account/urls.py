from django.urls import path
from account.views import loginView, registerView

urlpatterns = [
    path('', loginView, name="login"),
    path('registrieren', registerView, name="registrieren")
]