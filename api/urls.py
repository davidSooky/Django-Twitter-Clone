from django.urls import path
from . import viewsets

urlpatterns = [
    path("posts/", viewsets.post_all, name="posts"),
    path("user/<str:pk>/posts/", viewsets.users_posts, name="users_posts"),
    path("user/<str:pk>/followed_posts/", viewsets.followed_users_posts, name="followed_users_posts"),
    path("likes/create/", viewsets.create_like, name="create-like"),
    path("likes/delete/<str:pk>", viewsets.delete_like, name="delete-like"),
    path("follower/create/", viewsets.create_follower, name="create-follower"),
    path("follower/delete/<str:pk>", viewsets.delete_follower, name="delete-follower")
]