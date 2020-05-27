from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("register_client", views.register_client, name="register_client"),
    path("logout_view", views.logout_view, name="logout"),
    path("prebasket", views.prebasket, name="prebasket"),
    path("basket", views.basket, name="basket"),
    path("confirmation", views.confirmation, name="confirmation"),
    path("order_history", views.order_history, name="order_history"),
    path("confirmation/<order_id>", views.confirmation, name="order_info")
    # not sure about the below and about settings.py LOGIN_URL path
    #path('accounts/login/', auth_views.LoginView.as_view())
]
