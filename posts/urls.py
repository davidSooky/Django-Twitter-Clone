from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("<str:pk>/comments/", views.comment_view, name="comments"),
]