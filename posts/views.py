from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

# Model and form import
from .models import Post, Comment
from user.models import Profile
from .forms import CommentForm, TweetForm
from user.utils import get_recommended_users


# View to show comments of selected tweet
def comment_view(request, pk):
    post = Post.objects.get(id=pk)
    user = Profile.objects.get(user=request.user)
    comments = Comment.objects.filter(post=pk)
    owner = Profile.objects.get(user__username=post.owner.user)
    rec_users = get_recommended_users(user)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.post = post
            instance.save()
            return redirect("posts:comments", pk=pk)
    else:
        form = CommentForm()
    context = {"form":form, "user":user, "comments":comments, "post":post, "owner":owner, "unfollowed_users":rec_users}
    return render(request, "posts/tweet_detail.html", context)

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect ("user:home")
