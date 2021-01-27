from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.home_view, name="home"),
    path('register/', views.login_register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    # path('<str:username>/', views.ProfileView.as_view(), name="profile"),
    path('<str:username>/', views.profile_view, name="profile"),
]
