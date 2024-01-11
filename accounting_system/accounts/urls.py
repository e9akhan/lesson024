from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('transaction/', views.transaction, name='transaction'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout')
]