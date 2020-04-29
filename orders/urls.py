from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("register_client", views.register_client, name="register_client"),
    path("logout_view", views.logout_view, name="logout"),
    path("prebasket", views.prebasket, name="prebasket")
    # not sure about the below and about settings.py LOGIN_URL path
    #path('accounts/login/', auth_views.LoginView.as_view())
]
