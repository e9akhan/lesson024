"""
    Module name :- urls
"""

from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("transaction/", views.transaction, name="transaction"),
    path("transaction_history/", views.transaction_history, name="transaction_history"),
    path("registration/", views.registration, name="registration"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]
